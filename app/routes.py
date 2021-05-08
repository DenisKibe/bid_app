from app.api.auth import SignupAPI, GetTokenAPI,EmailVerificationAPI,ResetPasswordAPI,ForgetPasswordAPI,PhoneVerificationAPI
from app.api.views import ProductsAPI, AccountDetailsAPI,UploadImageAPI,WalletDetailsAPI,BidAPI,AccountExtrasAPI,SendEmaiLAPI,VerifyEmailAPI,ResetForgotPasswordAPI,VerifySmsCode

def initialize_routes(api):
    api.add_resource(SignupAPI, '/api/auth/registerUser')
    api.add_resource(GetTokenAPI, '/api/auth/getToken')
    api.add_resource(ProductsAPI, '/api/products')
    api.add_resource(AccountDetailsAPI, '/api/accontInfo')
    api.add_resource(UploadImageAPI, '/api/uploadPic')
    api.add_resource(WalletDetailsAPI, '/api/wallet')
    api.add_resource(BidAPI,'/api/bid')
    api.add_resource(AccountExtrasAPI, '/api/account')
    api.add_resource(SendEmaiLAPI,'/api/sendemail')
    api.add_resource(EmailVerificationAPI,'/api/sendEmailVerification')
    api.add_resource(VerifyEmailAPI,'/api/verifyEmail')
    api.add_resource(ResetPasswordAPI,'/api/changePassword')
    api.add_resource(ForgetPasswordAPI,'/api/sendPasswordResetlink')
    api.add_resource(ResetForgotPasswordAPI,'/api/resetpassword')
    api.add_resource(PhoneVerificationAPI,'/api/sendSmsVerification')
    api.add_resource(VerifySmsCode,'/api/verifyCode')
