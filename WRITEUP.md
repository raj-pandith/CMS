# Write-up Template

### Analyze, choose, and justify the appropriate resource option for deploying the app.

*For **both** a VM or App Service solution for the CMS app:*
- *Analyze costs, scalability, availability, and workflow*

##  VM vs App Service for CMS Application

| Criteria        | Virtual Machine (VM)                                   | App Service                                      |
|----------------|--------------------------------------------------------|--------------------------------------------------|
| Setup Time | Slower setup and configuration                         | Quick and easy setup                             |
| Cost        | Higher cost needed to pay for full infrastructure 24/7          | Cost-efficient only pay for platform and also can scale down|
| Workflow    | Full control, but requires maintenance & patching      | Fully managed, no server maintenance             |
| Deployment  | Manual deployment and configuration                    | Easy deployment (GitHub and more)      |
| Security    | User responsible for OS & security updates             | Managed security and automatic patching          |
| Setup Time | Slower setup and configuration                         | Quick and easy setup                             |

---

- *Choose the appropriate solution (VM or App Service) for deploying the app*
    
    Going with App Service
    
- *Justify your choice*

  App Service is chosen as the preferred deployment solution for the Flask application.
I prefer App Service because it is faster to deploy compared to VM with the help of github and also built-in scaling and load balancing
is there in case of high traffic on my web application.

---

### Assess app changes that would change your decision.

*Detail how the app and any other needs would have to change for you to change your decision in the last section.* 

Currently, App Service is the preferred choice due to its simplicity, scalability, and managed environment. However, certain changes in the application or its requirements could lead to choosing a Virtual Machine instead.

---

## Possible Changes in the Application

- **Need for Custom Environment**  
  If the application requires specific OS-level configurations, custom libraries, or unsupported software, a Virtual Machine would be more suitable.

-  **Increased Application Complexity**  
  If the application evolves into a complex system with multiple services, background jobs, or tightly coupled components, more control via a VM may be required.

-  **Strict Security or Compliance Requirements**  
  If the application needs advanced security configurations, custom firewall rules, or private network setups beyond App Service capabilities.

-  **Advanced Networking Needs**  
  If deep integration with virtual networks, on-premise systems, or private endpoints is required.

-  **Consistently High Workload**  
  If the application experiences steady high traffic, using a VM could be more cost-effective and offer predictable performance.

---
