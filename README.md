## Attention

### request generation with hey
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
