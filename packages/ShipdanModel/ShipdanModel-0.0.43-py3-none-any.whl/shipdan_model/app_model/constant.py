""" payment """
class DietPaymentScheduleStatus:
    UNDEFINED = 0
    REGISTERED = 1
    DIET_CREATE_COMPLETE = 2
    DIET_CREATE_FAILED = 3
    PAYMENT_COMPLETE = 4
    PAYMENT_FAILED = 5
    SKIP = 6
    PAYMENT_CANCEL = 7
    CANCEL = -1


DIET_PAYMENT_SCHEDULE_STATUS = (
    (DietPaymentScheduleStatus.UNDEFINED, '미정'),
    (DietPaymentScheduleStatus.REGISTERED, '등록'),
    (DietPaymentScheduleStatus.DIET_CREATE_COMPLETE, '식단 생성 성공'),
    (DietPaymentScheduleStatus.DIET_CREATE_FAILED, '식단 생성 실패'),
    (DietPaymentScheduleStatus.PAYMENT_COMPLETE, '결제 성공'),
    (DietPaymentScheduleStatus.PAYMENT_FAILED, '결제 실패'),
    (DietPaymentScheduleStatus.SKIP, '건너뜀'),
    (DietPaymentScheduleStatus.PAYMENT_CANCEL, '결제 취소'),
    (DietPaymentScheduleStatus.CANCEL, '해지'),
)


""" health """
class FoodProductTasteScoreStatus:
    UNDEFINED = 0
    BAD = 1
    NEUTRAL = 2
    GOOD = 3


FOOD_PRODUCT_TASTE_SCORE_STATUS = (
    (FoodProductTasteScoreStatus.UNDEFINED, '미정'),
    (FoodProductTasteScoreStatus.BAD, '나쁨'),
    (FoodProductTasteScoreStatus.NEUTRAL, '보통'),
    (FoodProductTasteScoreStatus.GOOD, '좋음'),
)

class DietPlanCreateOptionCode:
    ''' (23.12.29) 데이터가 별로 없기 때문에 일단은 constant로 관리 '''
    BOOKMARK = 1
    GOOD_SCORE = 2


""" food_payment """
class FoodOrderStatus:
    UNDEFINED = 0
    ORDER_COMPLETE = 1
    PAYMENT_COMPLETE = 2
    DELIVERY_COMPLETE = 3
    CANCEL_ORDER = -10

    FAIL = -20


FOOD_ORDER_STATUS = (
    (FoodOrderStatus.UNDEFINED, '미정'),
    (FoodOrderStatus.ORDER_COMPLETE, '주문완료'),
    (FoodOrderStatus.PAYMENT_COMPLETE, '결제완료'),
    (FoodOrderStatus.DELIVERY_COMPLETE, '배달완료'),
    (FoodOrderStatus.CANCEL_ORDER, '주문취소'),
    (FoodOrderStatus.FAIL, '문제상황'),
)


""" oms """
class FoodProductOrderLimitRequestStatus:
    UNDEFINED = 0  # 나중에 청사진이 필요해지면 사용
    REQUESTED = 1
    APPLIED = 2
    CHANGED = 3


FOOD_PRODUCT_ORDER_LIMIT_REQUEST_STATUS = (
    (FoodProductOrderLimitRequestStatus.UNDEFINED, '미정'),
    (FoodProductOrderLimitRequestStatus.REQUESTED, '요청 중'),
    (FoodProductOrderLimitRequestStatus.APPLIED, '적용 완료'),
    (FoodProductOrderLimitRequestStatus.CHANGED, '수정됨'),
)

""" food """
class LimitType:
    UNDEFINED = 0
    STORAGE = 1
    ROTATION = 2


LIMIT_TYPE = (
    (LimitType.UNDEFINED, '미정'),
    (LimitType.STORAGE, '재고형 limit'),
    (LimitType.ROTATION, '로테이션형 limit')
)
