from flask_restplus import Namespace

from resources.budget_limit_resource import BudgetLimitResource
from resources.budget_limit_update_resource import BudgetLimitUpdateResource
from resources.category_limit_resource import CategoryLimitResource
from resources.category_limit_update_resource import CategoryLimitUpdateResource
from resources.category_resource import CategoryResource
from resources.category_update_resource import CategoryUpdateResource
from resources.expense_resource import ExpenseResource
from resources.expense_update_resource import ExpenseUpdateResource
from resources.group_resource import GroupResource
from resources.group_update_resource import GroupUpdateResource
from resources.jwt_refresh_resource import JWTRefreshResource
from resources.login_jwt_resource import LoginJWTResource
from resources.login_resource import LoginResource
from resources.registration_email_resource import RegistrationEmailResource
from resources.send_registration_email_resource import SendRegistrationEmailResource
from resources.user_group_resource import UserGroupResource
from resources.user_group_update_resource import UserGroupUpdateResource
from resources.user_resource import UserResource
from resources.user_update_resource import UserUpdateResource
from utility.constants import Constants

namespace = Namespace('v1')
namespace.add_resource(UserResource, '/user')
namespace.add_resource(LoginResource, '/login')
namespace.add_resource(GroupResource, '/group')
namespace.add_resource(ExpenseResource, '/expense')
namespace.add_resource(CategoryResource, '/category')
namespace.add_resource(LoginJWTResource, '/login/jwt')
namespace.add_resource(UserGroupResource, '/user/group')
namespace.add_resource(UserUpdateResource, '/user/updates')
namespace.add_resource(BudgetLimitResource, '/group/limit')
namespace.add_resource(GroupUpdateResource, '/group/updates')
namespace.add_resource(JWTRefreshResource, '/login/jwt/refresh')
namespace.add_resource(CategoryLimitResource, '/category/limit')
namespace.add_resource(ExpenseUpdateResource, '/expense/updates')
namespace.add_resource(CategoryUpdateResource, '/category/updates')
namespace.add_resource(UserGroupUpdateResource, '/user/group/updates')
namespace.add_resource(BudgetLimitUpdateResource, '/group/limit/updates')
namespace.add_resource(CategoryLimitUpdateResource, '/category/limit/updates')
namespace.add_resource(SendRegistrationEmailResource, '/registration/sendemail')
namespace.add_resource(RegistrationEmailResource, Constants.registration_resource_path)
