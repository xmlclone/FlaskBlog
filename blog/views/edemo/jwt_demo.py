import logging

from flask import Blueprint, make_response
from flask_jwt_extended import jwt_required, create_access_token, current_user, set_access_cookies, unset_access_cookies

bp = Blueprint('jwt_demo', __name__, url_prefix='/demo/jwt_demo')

logger = logging.getLogger('jwt_demo')

'''
jwt_manager = JWTManager()
@jwt_manager.user_identity_loader
def user_identity_lookup(user):
    logger.debug(f'user_identity_loader: {user}')
    return user

@jwt_manager.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # {'fresh': False, 'iat': 1663243159, 'jti': '349eb619-4833-4720-bd70-02d905abec03', 'type': 'access', 'sub': 1, 'nbf': 1663243159, 'exp': 1663244059}
    logger.debug(f'user_lookup_loader: {jwt_data}')
    identity = jwt_data["sub"]
    return identity
'''

@bp.route('/get_token')
def get_token():
    token = create_access_token(identity=1)
    return {
        'token': token
    }

@bp.route('/get_token2')
def get_token2():
    token = create_access_token(identity=1)
    resp = make_response({
        'token': token
    })
    # 响应内容设置cookies携带token
    # 那么对于jwt_required并且locations参数允许或者全局配置允许cookies的情况，浏览器会自动携带此cookies进行验证
    set_access_cookies(resp, token)
    # 如果退出登录，应该在在退出的时候响应清理cookies
    # unset_jwt_cookies(resp)
    return resp

@bp.route('/jwt1')
@jwt_required()
def jwt1():
    '''
    请求头携带:
    Authorization: Bearer $token

    以下的携带方式，均不需要像header一样加前缀，比如Bearer
    cookies携带:
    set_access_cookies(resp, token)/unset_jwt_cookies(resp)

    url携带: url?jwt=xxxxxxxxxxxxxx

    json携带: 响应格式需要符合{
        'body': {
            'access_token': xxx 参数
        }
    }
    '''
    #  1: <class 'werkzeug.local.LocalProxy'>
    # 其表现形式虽然是整型1，但是其是一个werkzeug的LocalProxy对象
    # 
    logger.debug(f'{current_user}: {type(current_user)}')
    return {
        'code': 200,
        'message': 'success'
    }

@bp.route('/jwt2')
@jwt_required()
def jwt2():
    resp = make_response({
        'code': 200,
        'message': 'success'
    })
    unset_access_cookies(resp)
    return resp
