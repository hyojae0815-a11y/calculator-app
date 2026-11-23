
import streamlit as st

# ---------------------------------
# 1. 화면 기본 설정
# ---------------------------------
st.set_page_config(
    page_title="하루 칼로리 계산기",
    page_icon="🥗",
    layout="centered"
)

st.title("🥗 하루 적정 칼로리 계산기")
st.write("나의 하루 적정 칼로리와 실제 섭취량을 비교해 보세요!")

st.divider()

# ---------------------------------
# 2. 데이터 구조 (리스트)
# ---------------------------------

# 활동량별 계산 계수
activity_list = ["거의 운동하지 않음", "가벼운 운동", "보통 운동", "많은 운동", "매우 많은 운동"]
activity_factor_list = [1.2, 1.375, 1.55, 1.725, 1.9]

# 입력 정보와 결과를 저장할 리스트
result_list = []

# ---------------------------------
# 3. 사용자 정보 입력
# ---------------------------------

st.subheader("👤 나의 신체 정보")

age = st.number_input(
    "나이 (세)",
    min_value=1,
    max_value=100,
    value=18
)

gender = st.selectbox(
    "성별",
    ["남성", "여성"]
)

height = st.number_input(
    "키 (cm)",
    min_value=50.0,
    max_value=250.0,
    value=170.0
)

weight = st.number_input(
    "몸무게 (kg)",
    min_value=10.0,
    max_value=300.0,
    value=60.0
)

activity = st.selectbox(
    "하루 활동량",
    activity_list
)

st.divider()

# ---------------------------------
# 4. 하루 섭취 칼로리 입력
# ---------------------------------

st.subheader("🍚 오늘의 칼로리 섭취량")

intake = st.number_input(
    "오늘 하루 동안 섭취한 총 칼로리 (kcal)",
    min_value=0,
    max_value=10000,
    value=1800
)

# ---------------------------------
# 5. 함수 (def)
# ---------------------------------

def calculate_calories(age, gender, height, weight, activity_factor):

    # 남성과 여성의 기초대사량 계산
    if gender == "남성":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    # 활동량을 반영한 하루 에너지 필요량 추정
    daily_calories = bmr * activity_factor

    return round(daily_calories)


# ---------------------------------
# 6. 계산 버튼 및 결과 출력
# ---------------------------------

if st.button("🔍 나의 하루 적정 칼로리 계산하기", use_container_width=True):

    # 잘못된 입력 확인
    if age <= 0 or height <= 0 or weight <= 0:
        st.error("신체 정보를 올바르게 입력해 주세요.")

    else:

        # 리스트에서 선택한 활동량의 계수 찾기
        activity_index = activity_list.index(activity)
        selected_factor = activity_factor_list[activity_index]

        # 함수 실행
        daily_calories = calculate_calories(
            age, gender, height, weight, selected_factor
        )

        # 적정 칼로리에서 실제 섭취 칼로리 빼기
        difference = daily_calories - intake

        # 결과를 리스트에 저장
        result_list = [
            ["하루 적정 칼로리", daily_calories],
            ["하루 실제 섭취 칼로리", intake],
            ["칼로리 차이", abs(difference)]
        ]

        st.divider()
        st.subheader("📊 나의 계산 결과")

        # 반복문을 사용하여 결과 출력
        for item in result_list:
            st.write(f"**{item[0]}:** {item[1]:,} kcal")

        st.divider()

        # 조건문을 사용하여 섭취량 비교
        if difference > 0:

            st.success(
                f"현재 섭취량은 추정 필요량보다 "
                f"{difference:,} kcal 적습니다."
            )

            st.write(
                f"추정 필요량과의 차이: {difference:,} kcal"
            )

        elif difference < 0:

            st.error(
                f"현재 섭취량은 추정 필요량보다 "
                f"{abs(difference):,} kcal 많습니다."
            )

            st.write(
                f"추정 필요량을 초과한 양: {abs(difference):,} kcal"
            )

        else:

            st.warning(
                "현재 섭취량과 추정 필요량이 같습니다!"
            )

        st.divider()
        st.caption(
            "※ 이 계산은 성인용 기초대사량 추정식을 이용한 학습용 참고 자료입니다. "
            "성장기 청소년에게 적합한 영양 섭취 기준이 아니며, "
            "식사량 조절의 근거로 사용하지 마세요."
        )
