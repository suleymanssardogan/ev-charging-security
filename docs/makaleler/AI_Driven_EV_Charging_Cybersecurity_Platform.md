# Enhancing the Detection of Cyber-Attacks to EV Charging Infrastructures Through AI Technologies

**Source**: Electronics (MDPI), November 2024
**DOI**: 10.3390/electronics14214321
**URL**: https://www.mdpi.com/2079-9292/14/21/4321

## Abstract
This research presents a modular AI-driven platform designed for detecting cyber-attacks on electric vehicle (EV) charging infrastructures. The platform combines real-time data collection tools with Long Short-Term Memory (LSTM) Autoencoder-based anomaly detection.

## Methodology

### Data Collection Architecture
1. **Tshark**: Network packet capture and analysis
2. **Nozomi Networks Guardian**: Industrial network monitoring and security
3. **ELK Stack**:
   - Elasticsearch for data storage and search
   - Logstash for data processing and transformation
   - Kibana for data visualization and analysis
4. **Apache Kafka**: Real-time data streaming and processing

### AI Detection System
- **Core Technology**: LSTM Autoencoder for unsupervised anomaly detection
- **Data Type**: Multivariate time-series data representing normal traffic patterns
- **Detection Method**: Analysis of reconstruction errors to identify anomalies
- **Training Approach**: Unsupervised learning on normal network behavior

## Experimental Results

### Performance Metrics
- **Accuracy**: 97.1%
- **Recall**: 98.6%
- **Precision**: 52%

### Detection Capabilities
- Successfully identified cyber-induced anomalies
- Detected operational anomalies in charging infrastructure
- Effective identification of DoS (Denial of Service) attack scenarios
- Demonstrated proactive threat detection capabilities

## Key Achievements

### Technical Contributions
1. **Modular Architecture**: Flexible integration of multiple data sources
2. **Real-time Processing**: Continuous monitoring and analysis capability
3. **Multi-source Integration**: Combining network, operational, and security data
4. **Scalable Solution**: Adaptable to different EV charging environments

### Practical Applications
- Smart energy system security
- Critical infrastructure protection
- Real-time threat monitoring
- Automated incident response

## Limitations and Future Work

### Current Limitations
- **Lower Precision (52%)**: Due to traffic variability in EV charging networks
- **False Positive Rate**: Need for refinement in distinguishing malicious from benign traffic
- **Environment Specificity**: May require adaptation for different charging infrastructures

### Improvement Areas
1. Enhanced feature engineering for better precision
2. Integration of additional data sources
3. Advanced ML techniques for reduced false positives
4. Extended validation across diverse EV charging scenarios

## Technical Architecture

### Data Pipeline
```
Network Traffic → Tshark → Kafka → Logstash → Elasticsearch
↓
LSTM Autoencoder → Anomaly Detection → Kibana Dashboard
```

### Security Focus Areas
- Network communication anomalies
- Charging protocol violations
- Unusual power consumption patterns
- Communication interruption detection

## Industry Impact
The research represents a significant advancement toward resilient and adaptive cybersecurity solutions for energy infrastructures, addressing the growing security concerns in smart grid and EV charging networks.

## Conclusion
The combination of flexible data integration and AI-driven analysis demonstrates the potential for creating robust cybersecurity frameworks for critical energy infrastructure, particularly in the rapidly expanding EV charging sector.

---
*Downloaded and summarized from MDPI Electronics Journal*