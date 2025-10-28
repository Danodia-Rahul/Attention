# ML Inference Monitoring Stack

This project sets up a complete monitoring and alerting stack for an ML inference service using Docker Compose. It includes Prometheus for metrics collection, Grafana for visualization, and Alertmanager for sending email notifications when services go down.

## Architecture

The following containers are started:

* **app** – ML inference API
* **prometheus** – Metrics collection
* **grafana** – Metrics visualization
* **alertmanager** – Alert handling and email notifications

## Prerequisites

Ensure the following ports are available on your host system:

* `3000` – Grafana
* `8000` – ML Inference API
* `9090` – Prometheus
* `9093` – Alertmanager

Requirements:

* Docker
* Docker Compose

---

## Environment Configuration

Before starting the containers, you must configure environment variables for email alerts.

### Step 1: Copy the Example File

```bash
cp .env.example .env
```

### Step 2: Update the `.env` File

Open the `.env` file and replace the placeholder values with your actual email credentials:

```env
SMTP_SMARTHOST=smtp.gmail.com:587
SMTP_FROM=yourEmail@gmail.com
SMTP_USERNAME=yourEmail@gmail.com
SMTP_PASSWORD=your_16_character_password
ALERT_TO=recipientEmail@gmail.com
```

### Notes

* If using Gmail, you must generate a **16-character App Password**.
* Do not use your regular Gmail password.
* Make sure 2-Step Verification is enabled on your Google account before generating an App Password.

---

## Start the Setup

Run the following command:

```bash
docker compose up -d
```

This will start the four containers:

* `app`
* `prometheus`
* `grafana`
* `alertmanager`

To verify that containers are running:

```bash
docker ps
```

---

## Trigger an Alert (Service Down Test)

To simulate a service failure:

```bash
docker stop app
```

After a short wait, Alertmanager will send an email notification indicating the service is down.

To restart the service:

```bash
docker start app
```

You can also test alerts by stopping Prometheus:

---

## Access the Services

* ML API: [http://localhost:8000/docs](http://localhost:8000)
* Prometheus: [http://localhost:9090](http://localhost:9090)
* Grafana: [http://localhost:3000](http://localhost:3000)
* Alertmanager: [http://localhost:9093](http://localhost:9093)

---

## Generate Load with hey

You can test the inference API using the `hey` load testing tool.

Example request:

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

This sends 100 POST requests to the `/predict` endpoint.

---

## Email Alerts

When a monitored service:

* Goes down
* Becomes unreachable
* Fails health checks

Alertmanager sends an email notification to the configured recipient.

---

## Stop the Stack

To stop all containers:

```bash
docker compose down
```

To stop and remove volumes:

```bash
docker compose down -v
```
