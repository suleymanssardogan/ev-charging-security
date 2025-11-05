# Log Anomaly Detection & EVSE Security Research Bibliography

## 2024-2025 Recent Research Papers

### General Log Anomaly Detection

#### 1. Impact of Log Parsing on Deep Learning-based Anomaly Detection (2024)
- **Journal**: Empirical Software Engineering
- **DOI**: 10.1007/s10664-024-10533-w
- **Description**: Comprehensive empirical study on log parsing impact using 13 parsing techniques and 7 anomaly detection methods (DeepLog, LogAnomaly, LogRobust, CNN, PLELog, SVM, RF)
- **URL**: https://link.springer.com/article/10.1007/s10664-024-10533-w

#### 2. OneLog: Towards End-to-End Software Log Anomaly Detection (2024)
- **Journal**: Automated Software Engineering
- **DOI**: 10.1007/s10515-024-00428-x
- **Description**: End-to-end approach using single deep neural network instead of traditional four-stage architecture
- **URL**: https://link.springer.com/article/10.1007/s10515-024-00428-x

#### 3. LogEDL: Log Anomaly Detection via Evidential Deep Learning (2024)
- **Journal**: Applied Sciences (MDPI)
- **DOI**: 10.3390/app14167055
- **Description**: Addresses new anomalies not present in training data using evidential deep learning
- **URL**: https://www.mdpi.com/2076-3417/14/16/7055

#### 4. System Logs Anomaly Detection: Are we on the right path? (2024)
- **Journal**: Applied Artificial Intelligence
- **DOI**: 10.1080/08839514.2024.2440692
- **Description**: Comprehensive review of current approaches including LogFit and fine-tuned language models
- **URL**: https://www.tandfonline.com/doi/full/10.1080/08839514.2024.2440692

#### 5. Deep Learning-based Anomaly Detection and Log Analysis for Computer Networks (2024)
- **Repository**: arXiv
- **ID**: 2407.05639
- **Description**: Fusion model integrating Isolation Forest, GAN, and Transformer architectures
- **URL**: https://arxiv.org/abs/2407.05639

#### 6. Log File Anomaly Detection Using Knowledge Graph Completion (2024)
- **Conference**: Proceedings of the 2024 8th International Conference on Deep Learning Technologies
- **DOI**: 10.1145/3695719.3695726
- **Description**: Converting log messages to knowledge graph triples for anomaly detection
- **URL**: https://dl.acm.org/doi/full/10.1145/3695719.3695726

#### 7. A Comprehensive Investigation of Anomaly Detection Methods (2024)
- **Journal**: IET Information Security
- **DOI**: 10.1049/2024/8821891
- **Description**: Survey of anomaly detection methods in deep learning and machine learning (2019-2023)
- **URL**: https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/2024/8821891

### EVSE & Electric Vehicle Charging Security

#### 8. CICEVSE2024 Dataset (2024)
- **Institution**: University of New Brunswick, Canadian Institute for Cybersecurity
- **Description**: Multi-dimensional dataset with OCPP and ISO15118 communication, power consumption, network traffic
- **URL**: https://www.unb.ca/cic/datasets/evse-dataset-2024.html

#### 9. Enhancing the Detection of Cyber-Attacks to EV Charging Infrastructures Through AI Technologies (2024)
- **Journal**: Electronics (MDPI)
- **DOI**: 10.3390/electronics14214321
- **Description**: AI-driven platform with LSTM Autoencoder achieving 97.1% accuracy, 98.6% recall
- **URL**: https://www.mdpi.com/2079-9292/14/21/4321

#### 10. Explainable Deep Learning for Cyber Attack Detection in Electric Vehicle Charging Stations (2024)
- **Conference**: 11th International Conference on Networking, Systems, and Security
- **DOI**: 10.1145/3704522.3704534
- **Description**: Deep Learning model for EVSE attack detection using CICEVSE2024 dataset, 97.15% accuracy
- **URL**: https://dl.acm.org/doi/10.1145/3704522.3704534

#### 11. Enhancing EV Charging Station Security Using a Multi-dimensional Dataset: CICEVSE2024 (2024)
- **Conference**: Data and Applications Security and Privacy XXXVIII
- **DOI**: 10.1007/978-3-031-65172-4_11
- **Description**: Multi-dimensional approach for EV charging station security using behavioral profiling
- **URL**: https://link.springer.com/chapter/10.1007/978-3-031-65172-4_11

#### 12. Online Machine Learning for Intrusion Detection in Electric Vehicle Charging Systems (2025)
- **Journal**: Mathematics (MDPI)
- **Description**: Adaptive Random Forest with drift detection achieving 0.9913 accuracy
- **URL**: https://www.mdpi.com/2227-7390/13/5/712

## Standards and Guidelines Referenced

### Security Standards
- **ISO/IEC 27001** - Information Security Management System
  - Article A.12.4: Log masking/anonymization requirements
- **OWASP Logging Cheat Sheet** - Secure logging practices

### EV Charging Standards
- **IEC 61851** - Electric vehicle conductive charging system
- **OCPP (Open Charge Point Protocol)** - Communication between charging stations and central systems
- **ISO 15118** - Vehicle-to-Grid communication interface

## Key Research Trends & Methodologies

### Deep Learning Techniques
- **Transformer-based models**: 11 out of 42 techniques
- **RNN/LSTM**: Majority of models for sequential log analysis
- **CNN**: Convolutional approaches for pattern recognition
- **Autoencoders**: Unsupervised anomaly detection
- **GAN**: Generative adversarial networks for synthetic data
- **Graph Neural Networks**: For structural log relationships

### Attack Types Addressed
- **Reconnaissance attacks**
- **Backdoor infiltration**
- **Cryptojacking**
- **Denial of Service (DoS)**
- **Protocol violations**
- **Communication interruptions**

### Evaluation Metrics
- **Accuracy**: 97.1% - 99.13% in recent EVSE studies
- **Precision**: 97.19% - 99.99%
- **Recall**: 97.15% - 99.14%
- **F1-Score**: 99.56%

## Datasets for Research

### Public Datasets
1. **CICEVSE2024** - EV charging station security dataset
2. **Various log datasets** mentioned in parsing impact studies
3. **Network traffic datasets** for EV infrastructure

### Attack Simulation Tools
- **Tshark** - Network packet capture
- **Nozomi Guardian** - Industrial cybersecurity
- **ELK Stack** - Elasticsearch, Logstash, Kibana
- **SNMP/Syslog** - System monitoring

## Future Research Directions

1. **End-to-end approaches** replacing multi-stage architectures
2. **Real-time adaptive systems** handling concept drift
3. **Explainable AI** for security decision making
4. **Cross-protocol analysis** (OCPP + ISO15118)
5. **Privacy-preserving** anomaly detection methods
6. **Edge computing** integration for real-time detection

---
*Last Updated: November 2024*
*Compiled from recent academic research and industry reports*