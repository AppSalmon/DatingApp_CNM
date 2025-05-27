import os
import requests
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render
from .models import Profile
from django.urls import reverse
import json
import datetime

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URL API Gemini
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def chatbot_page(request):
    """
    Render trang giao diện chatbot.

    :param request: Yêu cầu HTTP.
    :return: TemplateResponse chứa giao diện chatbot.
    """
    return render(request, "chatbot/chatbot.html")

@csrf_exempt
@login_required
def chatbot_view(request):
    """
    Xử lý yêu cầu từ người dùng gửi đến chatbot, gọi API Gemini và truy vấn cơ sở dữ liệu để tìm profile phù hợp.

    :param request: Yêu cầu HTTP chứa dữ liệu JSON từ người dùng.
    :return: JsonResponse chứa phản hồi của chatbot.
    """
    if request.method == "POST":
        try:
            # Lấy dữ liệu JSON từ request
            data = json.loads(request.body)
            user_input = data.get("message", "").strip()
            logger.info(f"Received input: {user_input}")

            # Ghi log trạng thái session
            logger.info(f"Session before check: chatbot_initialized = {request.session.get('chatbot_initialized')}")

            # Kiểm tra session để trả lời lời chào mặc định
            if not request.session.get("chatbot_initialized"):
                logger.info("Sending default greeting and initializing session")
                request.session["chatbot_initialized"] = True
                request.session.modified = True  # Đảm bảo session được lưu
                reply = "Xin chào! Tôi là trợ lý tìm kiếm của IUH Dating App. Hãy mô tả mẫu người bạn muốn tìm (ví dụ: nữ, tóc đen, cao trên 1m60, ở TP.HCM)."
                return JsonResponse({"reply": reply})

            # Ghi log xác nhận đã qua kiểm tra session
            logger.info("Session already initialized, proceeding to Gemini API")

            # Tạo prompt cho Gemini
            prompt = f"""
            Bạn là một trợ lý AI của IUH Dating App, hỗ trợ người dùng tìm kiếm hồ sơ phù hợp dựa trên mô tả của họ. 
            Dựa trên mô tả sau, phân tích và trả về các tiêu chí cụ thể để tìm kiếm trong cơ sở dữ liệu:
            - Giới tính (MALE, FEMALE, hoặc BOTH)
            - Tên người dùng (username, ví dụ: 'Tuan' nếu yêu cầu tìm theo tên, khớp một phần, không phân biệt hoa thường)
            - Màu tóc (BLACK, BLONDE, BROWN, RED, GREY, BALD, BLUE, PINK, GREEN, PURPLE, OTHER)
            - Chiều cao (số cm, ví dụ: >160)
            - Vị trí (tên thành phố hoặc khu vực, ví dụ: Ho Chi Minh)
            - Độ dài tóc (LONG, SHOULDER_LENGTH, AVERAGE, SHORT, SHAVED)
            - Kiểu cơ thể (THIN, AVERAGE, FIT, MUSCULAR, A_LITTLE_EXTRA, CURVY; ánh xạ 'body đẹp' thành 'FIT' hoặc 'MUSCULAR')
            - Tình trạng hôn nhân (NEVER_MARRIED, DIVORCED, WIDOWED, SEPARATED)
            - Học vấn (HIGH_SCHOOL, COLLEGE, BACHELORS_DEGREE, MASTERS, PHD_POST_DOCTORAL; 'học đại học' ánh xạ thành 'BACHELORS_DEGREE')
            - Tuổi (khoảng tuổi, ví dụ: >18 hoặc 20-30)

            Mô tả của người dùng: {user_input}

            Trả về định dạng JSON với các tiêu chí, ví dụ:
            ```json
            {{
                "gender": "FEMALE",
                "username": null,
                "hair_colour": null,
                "height_min": null,
                "location": null,
                "hair_length": "LONG",
                "body_type": null,
                "relationship_status": null,
                "education": "BACHELORS_DEGREE",
                "age_min": 18,
                "age_max": null
            }}
            ```
            Nếu tiêu chí nào không được đề cập, để giá trị là null.
            """
            # Ghi log trước khi gọi Gemini
            logger.info("Calling Gemini API")
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            headers = {
                "Content-Type": "application/json"
            }

            try:
                response = requests.post(
                    f"{GEMINI_API_URL}?key={settings.GEMINI_API_KEY}",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                gemini_response = response.json()
                logger.info(f"Gemini response: {gemini_response}")
                # Kiểm tra cấu trúc phản hồi
                content = gemini_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "{}")
                try:
                    criteria = json.loads(content.strip("```json\n").strip("\n```"))
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON from Gemini: {content}")
                    return JsonResponse({"reply": "Lỗi xử lý phản hồi từ AI. Vui lòng thử lại!"}, status=500)
            except requests.exceptions.RequestException as e:
                logger.error(f"Error calling Gemini API: {str(e)}")
                return JsonResponse({"reply": f"Lỗi kết nối với AI: {str(e)}"}, status=500)

            # Truy vấn cơ sở dữ liệu dựa trên tiêu chí
            profiles = Profile.objects.filter(is_verified="APPROVED")
            logger.info(f"Initial profiles count: {profiles.count()}")

            # Ghi log tiêu chí từ Gemini
            logger.info(f"Criteria from Gemini: {criteria}")

            if criteria.get("gender"):
                gender = criteria["gender"].upper()
                profiles = profiles.filter(gender=gender)
                logger.info(f"After gender filter ({gender}): {profiles.count()} profiles")

            if criteria.get("username"):
                username = criteria["username"].strip()
                profiles = profiles.filter(user__username__icontains=username)
                logger.info(f"After username filter ({username}): {profiles.count()} profiles")

            if criteria.get("hair_colour"):
                hair_colour = criteria["hair_colour"].upper()
                profiles = profiles.filter(hair_colour__iexact=hair_colour)
                logger.info(f"After hair_colour filter ({hair_colour}): {profiles.count()} profiles")

            if criteria.get("height_min"):
                try:
                    height_min = float(criteria["height_min"])
                    profiles = profiles.filter(height__gte=height_min)
                    logger.info(f"After height_min filter (>{height_min}): {profiles.count()} profiles")
                except ValueError:
                    logger.error(f"Invalid height_min: {criteria['height_min']}")

            if criteria.get("location"):
                location = criteria["location"].strip()
                profiles = profiles.filter(location__icontains=location)
                logger.info(f"After location filter ({location}): {profiles.count()} profiles")

            if criteria.get("hair_length"):
                hair_length = criteria["hair_length"].upper()
                profiles = profiles.filter(hair_length__iexact=hair_length)
                logger.info(f"After hair_length filter ({hair_length}): {profiles.count()} profiles")

            if criteria.get("body_type"):
                body_type = criteria["body_type"].upper()
                profiles = profiles.filter(body_type__iexact=body_type)
                logger.info(f"After body_type filter ({body_type}): {profiles.count()} profiles")

            if criteria.get("relationship_status"):
                relationship_status = criteria["relationship_status"].upper()
                profiles = profiles.filter(relationship_status__iexact=relationship_status)
                logger.info(f"After relationship_status filter ({relationship_status}): {profiles.count()} profiles")

            if criteria.get("education"):
                education = criteria["education"].upper()
                profiles = profiles.filter(education__iexact=education)
                logger.info(f"After education filter ({education}): {profiles.count()} profiles")

            if criteria.get("age_min") or criteria.get("age_max"):
                today = datetime.date.today()
                if criteria.get("age_min"):
                    try:
                        age_min = int(criteria["age_min"])
                        max_birth_date = today - datetime.timedelta(days=age_min * 365.25)
                        profiles = profiles.filter(birth_date__lte=max_birth_date, birth_date__isnull=False)
                        logger.info(f"After age_min filter (>{age_min}): {profiles.count()} profiles")
                    except ValueError:
                        logger.error(f"Invalid age_min: {criteria['age_min']}")
                if criteria.get("age_max"):
                    try:
                        age_max = int(criteria["age_max"])
                        min_birth_date = today - datetime.timedelta(days=age_max * 365.25)
                        profiles = profiles.filter(birth_date__gte=min_birth_date, birth_date__isnull=False)
                        logger.info(f"After age_max filter (<{age_max}): {profiles.count()} profiles")
                    except ValueError:
                        logger.error(f"Invalid age_max: {criteria['age_max']}")

            # Tạo phản hồi với link profile
            if profiles.exists():
                reply = "Dựa trên yêu cầu của bạn, tôi đã tìm thấy các hồ sơ phù hợp:\n\n"
                for profile in profiles[:5]:  # Giới hạn 5 kết quả
                    profile_url = f"http://127.0.0.1:8000/profiles/member/{profile.user.id}/"
                   
                    reply += (
                        f"- **[{profile.user.username}]({profile_url})**: "
                        f"{profile.age()} tuổi, {profile.get_gender_display()}, "
                        f"{profile.get_hair_colour_display()} tóc {profile.get_hair_length_display().lower()}, "
                        f"{profile.get_body_type_display().lower()}, "
                        f"{profile.get_education_display().lower()}, "
                        f"{profile.get_relationship_status_display().lower()}, "
                        f"ở {profile.location}\n"
                    )
                reply += "\nBạn có muốn tôi tìm thêm hoặc lọc thêm tiêu chí không?"
            else:
                reply = "Xin lỗi, tôi không tìm thấy hồ sơ nào phù hợp với tiêu chí của bạn. Hãy thử mô tả lại hoặc nới lỏng tiêu chí nhé!"

            return JsonResponse({"reply": reply})

        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body")
            return JsonResponse({"reply": "Dữ liệu không hợp lệ. Vui lòng thử lại!"}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({"reply": f"Lỗi hệ thống: {str(e)}"}, status=500)
    return JsonResponse({"reply": "Phương thức không được hỗ trợ"}, status=405)