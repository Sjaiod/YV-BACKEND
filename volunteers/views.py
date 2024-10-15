from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from .utils.volunteer_helpers import create_new_volunteer_sheet, stop_volunteer_intake
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import VolunteerIntakeStatus  # Import the model
from django.shortcuts import redirect, render
from utils.bkash_payment_middilware import bkash_genarate_token ,bkash_create_payment,bkash_execute_payment
from decouple import config
import requests
class StartVolunteerIntakeView(APIView):
    def post(self, request):
        # Logic to start the intake and create a new sheet
        file_path = create_new_volunteer_sheet()
        # Set intake status to open, updating or creating the entry
        VolunteerIntakeStatus.objects.update_or_create(
            is_open=True, 
            defaults={'current_sheet_id': file_path}  # Update with the new file path
        )
        return Response({"message": "Volunteer intake started", "file_path": file_path})

class StopVolunteerIntakeView(APIView):
    def post(self, request):
        # Logic to stop intake and upload to Google Drive
        intake_status = VolunteerIntakeStatus.objects.filter(is_open=True).first()
        if intake_status:
            file_url = stop_volunteer_intake(intake_status.current_sheet_id)
            intake_status.is_open = False
            intake_status.save()
            return Response({"message": "Volunteer intake stopped", "file_url": file_url})
        return Response({"error": "No active intake to stop"}, status=400)
    

class TokenGenarateView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        id=request.data.get("id")
        if not id:
            return Response({"error":"NO id was provided"},status=401)
        else:

            bkash_genarate_token(id)
            return Response({"OK"},status=500)

class BkashPaymentCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        if not data:
            return Response({"error": "NO DATA was provided"}, status=401)
        else:
            token = bkash_genarate_token(id=data.get('id'))
            if token:
                base_url = config("URL")
                call_back_url = f"{base_url}/api/vol/payment/callback/?token={token}&name={data.get('name')}&email={data.get('email')}&phone={data.get('phone')}&bloodGroup={data.get('bloodGroup')}"
                create_payment = bkash_create_payment(id=token, amount=data.get('amount'), callback_url=call_back_url)
                
                if create_payment:
                    return redirect(create_payment)  # Redirect to the payment URL
                else:
                    return Response({"error": "Faced some error"}, status=501)
            else:
                return Response({"error": "Invalid Token"})

class BkassCallBackView(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
     # Accessing the 'paymentID' and 'token' from the query parameters
        payment_id = request.query_params.get('paymentID')
        token = request.query_params.get('token')  # Retrieving the token passed in the URL
        status = request.query_params.get('status')
        name=request.query_params.get('name')
        email=request.query_params.get('email')
        phone=request.query_params.get('phone')
        blood_group=request.query_params.get('bloodGroup')

        if status in ["failure", "cancel"]:
            # Redirecting to "/error" in case of failure or cancel status
            error_redirect_url=f"{config("FRONTEND_URL")}/youthvoice/volentier/error"
            return redirect(error_redirect_url)

        elif status == "success":
            # Call bkash_execute_payment using the token retrieved from the URL
            execute_payment_response = bkash_execute_payment(token, payment_id)
            
            if execute_payment_response:
                exe_payment_status=execute_payment_response.get('statusCode')
                paymen_id=execute_payment_response.get('paymentID')
                if exe_payment_status == "0000":
                    base_url=config("URL")
                    response=requests.post(url=f"{base_url}/api/vol/create",json={
                        "name":name,
                        "email":email,
                        "phone":phone,
                        "bloodGroup":blood_group
                    })
                    if response:
                        response_data=response.json()
                        if(response_data):

                           success_redirect_url=f"{config('FRONTEND_URL')}/youthvoice/volentier/success"
                           return redirect(success_redirect_url)
                        else:
                            return Response({"Failed"},status=500)
                
            else:
                return Response({"error": "Payment execution failed"}, status=500)
            
class CreateVolentierViwe(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        data=request.data
        return Response({"data":data},status=200)