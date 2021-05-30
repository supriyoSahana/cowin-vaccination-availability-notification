# cowin-vaccination-availability-notification
```
Pre - req : twilio account
District_Id
Target Audience: < 45 yrs

Track District_Id:
1. Fire https://cdn-api.co-vin.in/api/v2/admin/location/states at your browser and grab your state Id.
2. Fire https://cdn-api.co-vin.in/api/v2/admin/location/districts/<StateId Tracked From step1>  and grab your District_id
```

```
Code Philisophy: If run in background it will keep hitting cowin API every 5 min to check vaccine availability for a week and will send a text notification [max 5 texts to avoid free twilio account burn out] and will get reset very next day.





