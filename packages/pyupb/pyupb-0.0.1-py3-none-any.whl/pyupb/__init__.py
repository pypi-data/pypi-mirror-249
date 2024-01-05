import threading
import requests
from datetime import datetime
import uuid
import jwt

__api_url = 'https://api.upbit.com/v1'
__last_request_timestamp:float = 0.0
__last_available_request_per_minute:int = 0
__last_available_request_per_second:int = 0

__stop_event = threading.Event()

def stop():
    global __stop_event
    __stop_event.set()

def get_need_sleep_seconds() -> float:
    global __last_available_request_per_minute
    global __last_available_request_per_second
    
    now = datetime.now().timestamp()
    sleep_seconds = 0.0
    if 0 < __last_request_timestamp:
        if __last_available_request_per_minute == 0:
            sleep_seconds = 61 - (now - __last_request_timestamp)
        elif __last_available_request_per_second == 0:
            sleep_seconds = 1 - (now - __last_request_timestamp)
            
    return sleep_seconds

def sleep_by_remain(sleep_seconds:float):
    return __stop_event.wait(sleep_seconds)

def __set_remain(headers):
    '''
    set remaining count per minute, second\n
    Parameters
    -
    headers(dict): response headers
    '''
    global __last_request_timestamp
    __last_request_timestamp = datetime.now().timestamp()
    
    global __last_available_request_per_minute
    global __last_available_request_per_second
    
    if 'Remaining-Req' in headers:
        temp_remaining_req = headers['Remaining-Req']
        temp_remaining_req_texts = temp_remaining_req.split(';')
        for remaining_req_text in temp_remaining_req_texts:
            remaining_req_var_vals = remaining_req_text.split('=')
            key = remaining_req_var_vals[0].replace(' ', '')
            value = remaining_req_var_vals[1].replace(' ', '')
            if key == 'min':
                __last_available_request_per_minute = int(value)
            elif key == 'sec':
                __last_available_request_per_second = int(value)
    
def get_codes(block:bool = True):
    market_all = get_market_all(block)
    codes = []
    for code_name_data in market_all:
        if 'market' in code_name_data and code_name_data['market'][:3] == 'KRW':
            code = code_name_data['market']
            codes.append(code)
    return codes

def get_market_all(block:bool = True):
    '''
    Get all market code information.
    
    Parameter
    -
        block(bool): sleep by avaliable call count. default True.
        
    Return
    -
        market(str): 업비트에서 제공중인 시장 정보
        korean_name(str): 거래 대상 암호화폐 한글명
        english_name(str): 거래 대상 암호화폐 영문명
        market_warning(str): 유의 종목 여부 NONE (해당 사항 없음), CAUTION(투자유의)
    '''
    result = {}
    is_terminated = False
    sleep_seconds = get_need_sleep_seconds()
    if block:
        if 0 < sleep_seconds:
            is_terminated = sleep_by_remain(sleep_seconds)
            sleep_seconds = 0
            
    if 0 == sleep_seconds and not is_terminated:
        response = requests.get(url=__api_url+"/market/all", headers={"Accept":"application/json"})
        __set_remain(response.headers)
        result = response.json()
    
    return result


def get_accounts(access_key:str, secret_key:str, block:bool = True):
    '''
    Parameter
    -
        access_key(str): access_key
        secret_key(str): secret_key
        block(bool): sleep by avaliable call count. default True.
    
    Return
    -
        currency(str): 화폐를 의미하는 영문 대문자 코드
        balance(str): 주문가능 금액/수량
        locked(str): 주문 중 묶여있는 금액/수량
        avg_buy_price(str): 매수평균가
        avg_buy_price_modified(bool): 매수평균가 수정 여부
        unit_currency(str): 평단가 기준 화폐
    '''
    
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
        'Authorization': authorization,
    }
    result = {}
    is_terminated = False
    sleep_seconds = get_need_sleep_seconds()
    
    if block:
        if 0 < sleep_seconds:
            is_terminated = sleep_by_remain(sleep_seconds)
            sleep_seconds = 0
            
    if 0 == sleep_seconds and not is_terminated:
        response = requests.get(__api_url+'/accounts', headers=headers)
        __set_remain(response.headers)
        result = response.json()
    
    return result