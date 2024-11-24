# **The Live Stream Pipeline**  

### **Description**  
Imagine tracking a car on its way from London to Birmingham in real-time. Sounds exciting, right? That's exactly what this project is about. Here's how it works:  

- **Collecting data**:  
  From IoT devices, we’ll capture live vehicle stats, GPS locations, emergency alerts, weather updates, and even camera footage.  

- **Moving the data**:  
  Tools like **Apache Kafka** and **Zookeeper** ensure this constant flow of information doesn’t hit a traffic jam.  

- **Processing the data**:  
  With **Apache Spark**, we’ll clean, analyze, and make sense of everything—fast.  

- **Storing it**:  
  All this information gets neatly organized in **AWS Redshift**, ready for use.  

- **Visualizing it**:  
  Finally, using **Power BI**, we’ll bring the data to life with easy-to-read charts and dashboards.  

### **Overview**  
This project simplifies real-time streaming from start to finish. Every phase—*from ingestion to processing to storage*—is designed to show how modern tools and cloud tech come together to solve real-world challenges.  

### **Project Goal**  
To build a comprehensive real-time data streaming pipeline that efficiently captures, processes, and visualizes data in a seamless end-to-end flow. 

# **Architecture Diagram**
![Architecture Diagram](https://github.com/user-attachments/assets/04f9eaf2-8584-4653-abae-983876923db0)


### **Technologies Used**

- **IoT Devices**: Capture real-time data, including vehicle stats, GPS locations, and sensor information.  
- **Apache Zookeeper**: Manage and coordinate Kafka brokers for seamless operation.  
- **Apache Kafka**: Ingest real-time data streams into various topics for processing.  
- **Apache Spark**: Perform real-time data transformation, processing, and streaming. Includes a **Spark Worker** for distributed computation and scalability.  
- **Docker**: Containerize and orchestrate Kafka and Spark for a consistent, scalable environment.  
- **Python**: Write custom scripts for data processing and integration.  

#### **AWS Cloud Services**  
- **S3**: Store processed data as Parquet files for efficient storage and access.  
- **Glue**: Extract, transform, and catalog data for downstream analysis.  
- **Athena**: Query processed data using serverless, SQL-based analytics.  
- **IAM**: Manage roles, permissions, and secure access to cloud resources.  
- **Redshift**: Store and analyze data in a scalable data warehouse.  

#### **Visualization**  
- **Power BI**: Create dashboards and visualizations to derive insights from Redshift data.

### **Project Workflow**

1. **Data Generation**  
   - Simulated data is generated using IoT devices, including vehicle stats, GPS data, emergency incidents, weather updates, and camera footage.

2. **Data Ingestion**  
   - Real-time data streams are ingested into **Apache Kafka** topics.  
   - **Apache Zookeeper** coordinates and manages the Kafka brokers for efficient data ingestion.  

3. **Data Processing**  
   - **Apache Spark** processes data in real time.  
   - The **Spark Worker** performs distributed computation for faster and scalable data transformation and aggregation.

4. **Data Storage**  
   - Processed data is saved in **AWS S3** as Parquet files for efficient storage.  
   - **AWS Glue** catalogs the data and prepares it for querying.  
   - Data is loaded into **AWS Redshift** for analytics and long-term storage.

5. **Data Analysis**  
   - **AWS Athena** enables ad hoc querying of processed data stored in S3.  
   - Redshift serves as the primary data warehouse for structured analysis.

6. **Data Visualization**  
   - **Power BI** connects to Redshift and creates dashboards and visualizations, providing insights into the data.

7. **Orchestration and Deployment**  
   - **Docker** ensures consistent and scalable deployment of Kafka, Spark, and other services.

### **Workflow Overview**

- Data flows from IoT devices → **Kafka topics** → **Spark processing** → **S3 storage** → **AWS Glue** → **Redshift** → **Power BI visualization**.
- The architecture is designed to handle real-time streaming, ensuring scalability and efficiency at every stage.  
  
### **Getting Started**  
This guide will help you set up and run the real-time data streaming pipeline. Follow the steps below to get started.  

---

### **Prerequisites**  
Before you begin, make sure you have the following:  
- **Docker Desktop**: Installed and running.  
- **AWS Account**: With appropriate IAM roles and permissions.  
- **Python 3.x**: Installed on your local machine.  
- **Apache Kafka and Apache Spark**: Pre-configured for use.  

---

### **Setup Instructions**  

#### 1. **Clone the Repository**   
  ```bash  
      git clone https://github.com/Shyam7926/The-Live-Stream-Pipeline.git  
      cd The-Live-Stream-Pipeline.
```
### 2. **AWS Configuration**

- **Update AWS Credentials**  
   Update the `config.py` file with your AWS Access Key and Secret Key details.

- **Create an S3 Bucket**  
   Create an S3 bucket to store raw and processed data.

- **Set Up Public Access Policy**  
   Use the [AWS Policy Generator](https://awspolicygen.s3.amazonaws.com/policygen.html) to create a public access policy for the S3 bucket.

- **Set Up AWS Glue Crawlers**  
   Configure AWS Glue crawlers to catalog your raw and processed data in S3.

- **Configure Athena**  
   Use Athena to query the cataloged data in S3.

- **Create Redshift Cluster**  
   Create a Redshift cluster to store processed data for structured analysis. Redshift will allow you to perform complex queries on large datasets and integrate with tools like Power BI for visualization.

#### 3. **Configure Docker**
- Ensure Docker desktop installed and running.
- Open the docker-compose.yml file and configure services for Kafka and Spark.
- Start Docker Engine:
```
docker-compose up -d  
```
#### 4. **Install Dependencies**
- Use the requirements.txt file to install dependencies:
```
pip install -r requirements.txt  
```
#### 5. **Run Data Ingestion**
- Produce data to Kafka topics using IoT data simulators:

bash
```
python main.py
```
#### 6. **Verify Kafka Setup**
- Check if the Kafka broker is receiving data:

bash
```
kafka-topics --list --bootstrap-server broker:29092
```
```
kafka-console-consumer --topic vehicle_data --bootstrap-server broker:9092 --from-beginning
``` 
![image](https://github.com/user-attachments/assets/fa19f455-01f7-4bb1-a8e9-eeac6fc9bd6a)


#### 7. **Run Spark Streaming**
- Submit the Spark job to process and stream data:

bash
```
docker exec -it realtime-streaming-pipeline-spark-master-1 spark-submit \
--master spark://spark-master:7077 \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk:1.11.469 \
/opt/bitnami/spark/jobs/spark-stream.py  
```
![Writing Data to S3](https://github.com/user-attachments/assets/767a0acd-e749-42e1-b775-b3721ec74023)

#### 8. **Set Up Glue and Athena**
- Check the data in S3
![data in s3](https://github.com/user-attachments/assets/0767368a-efd0-454e-bae6-768a4dfe1372)

- Create Glue crawlers to catalog processed data.
- Use Athena to query cataloged data stored in S3.
![Data Querying on Athena](https://github.com/user-attachments/assets/5cace0bb-755c-4526-a94e-2989a59c9628)


#### 9. **Use Redshift for Data Warehousing**
- Load processed data into AWS Redshift for structured analysis.
- Ensure your Redshift cluster is configured and accessible.

#### 10. **Visualize Data with Power BI**
- Connect Power BI to Redshift.
- Build interactive dashboards and visualizations to derive insights from the data.

#### **Example Flow of Dashboard:**

| Section                  | Visual Type      | Key Insights                                |
|--------------------------|------------------|---------------------------------------------|
| Vehicle Overview         | Cards, KPIs      | Average Speed, Total Incidents, Total Distance Covered |
| Journey on the Map       | Map              | Visualize the path with speed and weather overlays |
| Emergency Details        | Table, Cards     | List of incidents with descriptions         |
| Performance Trends       | Line Chart       | Speed trends over time                      |
| Weather & Traffic Insights | Bar Chart, Images | Analyze weather patterns and traffic snapshots |

- This design will ensure you deliver a highly interactive, visually appealing, and insightful Power BI dashboard! 







