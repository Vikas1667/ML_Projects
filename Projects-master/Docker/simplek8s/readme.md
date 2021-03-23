
## Client-pod.yaml
![image1](images/client_pod_yaml_code.jpg)


## Client-node-pod.yaml

![image2](images/client_node_pod_yaml_code.jpg)


•	Kind: Type of object in k8 in cluster
Subtypes or obj type of service:

1)	ClusterIP
2)	NodePort: Exposes a container to outside world (only good for dev purposes)
3)	LoadBalancer
4)	Ingress


•	Version: Different set of object or scopes of types of objects to specify
•	Selector: Label selector property to link object
              specify to send traffic to client pod
•	Ports: All port to be open & mapped to target 
•	NodePort: URL port range (30000,32767) not always to specify. 



|kubectl	| apply | -f	| filename|
------- | ---------|-----|-----------| 
|CMD    | Change configuration of Cluster| we want to specify a file that has the config changes|


![image3](images/client_pod_yaml.png)

![image4](images/client_node_pod_yaml.jpg)
 

 |kubectl	|get 	|pods|
 |-----   |-----|----|
 |      |We want to retrieve information| specifies object type about running object 
 
![image5](images/get_pods.jpg)
 
 
![image6](images/localhost.png)

![image7](images/ip.jpg)

![image3](images/minikube_service_list.jpg)


![image3](images/app.jpg)

Issue 
https://stackoverflow.com/questions/62375642/minikube-ip-returns-127-0-0-1-kubernetes-nodeport-service-not-accessable
