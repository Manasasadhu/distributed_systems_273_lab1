Distributed Systems Lab 1 - Week 1

## How to run locally:

Clone the repository and understand the requirements for each service. And follow the steps below to run the services locally.

### Testing the services:

1. Start service A (provider_service)
   ```bash
   cd provider_service
   pip install -r requirements.txt
   python app.py
   ```
2. Start service B (consumer_service) in a new terminal
   ```bash
   cd consumer_service
   pip install -r requirements.txt
   python app.py
   ```
3. Test service A health check
8080 Health Check 

<img width="644" height="165" alt="image" src="https://github.com/user-attachments/assets/785296fe-3dd8-47d1-8c58-9433d36e16b7" />
<img width="1041" height="489" alt="image" src="https://github.com/user-attachments/assets/c166dcdf-4bfd-4c4a-b7f4-a94f306c5724" />

4. Test service A echo endpoint
8080 Echo call 

<img width="1060" height="493" alt="image" src="https://github.com/user-attachments/assets/b3c1af9a-282a-4de2-8d5c-e95318b98b37" />

5. Test service B health check
8081 Health Check

<img width="1067" height="530" alt="image" src="https://github.com/user-attachments/assets/3d52e066-88b5-41a8-9785-be8d2febb0ba" />

6. Test service B calling service A

**Success Scenario **- Calling service_a(8080) from service_b(8081) when both services are up

<img width="1060" height="585" alt="image" src="https://github.com/user-attachments/assets/c36bc957-84d7-43b6-929a-27b786da52e7" />

**Failure Scenario** - Calling service_a(8080) from service_b(8081) when service_a is down

<img width="1036" height="601" alt="image" src="https://github.com/user-attachments/assets/4ecf8ee7-b401-4d6f-9f6c-7e150c0d0539" />

## Why is this distributed??

The system is distributed because it consists of two independent services (service A/provider_service and service B/consumer_service) that communicate over a network using HTTP requests. Each service runs independently as if they are running on two different machines/containers, even though on a same machine and they interact with each other's requests. This independence and network communication are key characteristics of distributed systems.
