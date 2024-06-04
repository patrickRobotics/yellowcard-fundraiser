This is a Python Flask app

### Environment setup
To access YellowCard APIs, you need an api_key and a secret_key which should be saved in a .env file
1. Create a file named *.env* and save the keys there
```
API_KEY=<YELLOW_CARD_SANDBOX_API_KEY>
SECRET_KEY=<YELLOW_CARD_SANDBOX_SECRE_KEY>
```
2. Create and activate a virtualenv

3. Start the application. Inside the virtual environment, run python main.py and access the app on http://127.0.0.1:5000/
   ![image](https://github.com/patrickRobotics/yellowcard-fundraiser/assets/4558053/fc54b12f-10fe-4c4c-9602-cea70cce79b5)

5. Create a Fundraising campaign
   
  ![image](https://github.com/patrickRobotics/yellowcard-fundraiser/assets/4558053/38b4d172-ae77-40b5-99e3-a0254d2504c3)
  ![image](https://github.com/patrickRobotics/yellowcard-fundraiser/assets/4558053/a4d6cdaf-6206-404d-aebc-b2214a271ba0)

7. Receive donations: Navigate to View all funds and click Donate
   This uses YellowCard's /collections API to make a POST request and save the donation data
   The use case is to POST a collection request to the user's YellowCard wallet that will deposit onto the Fundraiser account
   whose details have been hard-coded in the recipient's data, towards achieving the fundraiser's goal.

  ![image](https://github.com/patrickRobotics/yellowcard-fundraiser/assets/4558053/aa960af2-dc8b-4265-9e2f-df41c3c41224)
  ![image](https://github.com/patrickRobotics/yellowcard-fundraiser/assets/4558053/69ac60ee-64e5-4d8f-84e0-3263feadd586)

