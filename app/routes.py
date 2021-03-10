from app.api.auth import SignupAPI, GetTokenAPI
from app.api.views import ProductsAPI, AccountDetailsAPI,UploadImageAPI,WalletDetailsAPI,BidAPI

def initialize_routes(api):
    api.add_resource(SignupAPI, '/api/auth/registerUser')
    api.add_resource(GetTokenAPI, '/api/auth/getToken')
    api.add_resource(ProductsAPI, '/api/products')
    api.add_resource(AccountDetailsAPI, '/api/accontInfo')
    api.add_resource(UploadImageAPI, '/api/uploadPic')
    api.add_resource(WalletDetailsAPI, '/api/wallet')
    api.add_resource(BidAPI,'/api/bid')