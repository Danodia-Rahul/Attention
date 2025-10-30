# ML Inference API Observability Stack

Modern machine learning services require visibility into request volume, latency, availability, and failure rates to ensure reliability in production environments.

This project demonstrates how to build a lightweight observability stack around an ML inference API using:

* **Prometheus** for metrics collection
* **Grafana** for visualization
* **Alertmanager** for alert handling and notifications
* A containerized ML inference API

The stack monitors service health and automatically triggers email alerts when availability or error thresholds are breached.

---

# Architecture

The system consists of four containers:

| Container        | Purpose                               |
| ---------------- | ------------------------------------- |
| **app**          | ML inference API                      |
| **prometheus**   | Metrics scraping and storage          |
| **grafana**      | Metrics dashboards and visualization  |
| **alertmanager** | Alert routing and email notifications |

All services are orchestrated using Docker Compose.

---

# Prerequisites

Ensure the following ports are available on your host machine:

* `3000` – Grafana
* `8000` – ML Inference API
* `9090` – Prometheus
* `9093` – Alertmanager

### Requirements

* Docker
* Docker Compose

---

# Environment Configuration

Email alerts require SMTP configuration.

## Step 1: Copy the Example Environment File

```bash
cp .env.example .env
```

## Step 2: Update the `.env` File

Replace the placeholder values with your actual email credentials:

```env
SMTP_SMARTHOST=smtp.gmail.com:587
SMTP_FROM=yourEmail@gmail.com
SMTP_USERNAME=yourEmail@gmail.com
SMTP_PASSWORD=your_16_character_app_password
ALERT_TO=recipientEmail@gmail.com
```

### Important Notes

* If using Gmail, generate a **16-character App Password**.
* Do not use your regular Gmail password.
* Enable 2-Step Verification before generating an App Password.

---

# Start the Stack

Launch all services in detached mode:

```bash
docker compose up -d
```

Verify running containers:

```bash
docker ps
```

You should see:

* app
* prometheus
* grafana
* alertmanager

---

# Metrics Exposed by the Application

The ML API exposes Prometheus-compatible metrics using `prometheus-client`.

### Available Metrics

| Metric                            | Description                     |
| --------------------------------- | ------------------------------- |
| `total_app_requests_total`        | Total number of API requests    |
| `application_request_error_total` | Total number of failed requests |
| `up`                              | Service availability status     |

These metrics are scraped by Prometheus and visualized in Grafana.

---

# Alert Rules

The system triggers alerts under the following conditions:

### 1. Service Down Alert

* If `app` or `prometheus` is down for more than **1 minute**
* Alert is fired and routed to Alertmanager
* Email notification is sent

### 2. High Error Rate Alert

* If API error rate exceeds **5%**
* Alert is triggered
* Email notification is sent

---

# Simulating Failures

## Service Down Test

Stop the application container:

```bash
docker stop app
```

After approximately one minute, an email alert will be triggered.

Restart the container:

```bash
docker start app
```

---

## High Error Rate Test

Use the `hey` load testing tool to intentionally send malformed requests.

Example:

```bash
hey -z 2m \
  -m POST \
  -H "Content-Type: application/json" \
  -d '{
  "Age": 20,
  "Income": 100000,
  "Dependents": 3,
  "Occupation": "NOTTHERE",
  "Credit": 1000,
  "Property": "House"
}' \
http://localhost:8000/predict
```

This generates traffic for 2 minutes and forces validation errors, increasing the error rate above the alert threshold.

---

# Accessing the Services

* ML API: [http://localhost:8000/docs](http://localhost:8000/docs)
* Prometheus: [http://localhost:9090](http://localhost:9090)
* Grafana: [http://localhost:3000](http://localhost:3000)
* Alertmanager: [http://localhost:9093](http://localhost:9093)

---

# Load Testing Example

Send 100 valid prediction requests:

```bash
hey -n 100 \
  -m POST \
  -H "Content-Type: application/json" \
  -d '{
  "Age": 20,
  "Income": 100000,
  "Dependents": 3,
  "Occupation": "Employed",
  "Credit": 1000,
  "Property": "House"
}' \
http://localhost:8000/predict
```

---

# Email Alert Behavior

Alertmanager sends email notifications when:

* A service becomes unavailable
* A container is unreachable
* Health checks fail
* Error rate exceeds the configured threshold

Alerts automatically resolve when the system returns to a healthy state.

---

# Stop the Stack

Stop all services:

```bash
docker compose down
```

Stop and remove volumes:

```bash
docker compose down -v
```

---

# What This Project Demonstrates

* Production-grade monitoring for ML inference APIs
* Real-time metrics collection
* Error-rate-based alerting
* Container health monitoring
* Automated email notifications
* Observability best practices for ML systems
