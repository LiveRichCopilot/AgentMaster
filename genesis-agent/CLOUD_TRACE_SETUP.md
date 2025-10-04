# 📊 Cloud Trace Setup for JAi Cortex OS

## ✅ Tracing is NOW ENABLED

Your Agent Development Kit now has **Cloud Trace enabled** to monitor:
- ✅ Which specialist agents are called (CodeMaster, CloudExpert, etc.)
- ✅ Tool execution timeline and performance
- ✅ LLM interaction response times
- ✅ Complete request flow from user query to final response
- ✅ Delegation to Vertex AI deployed agents

---

## 🔍 What You'll See in Traces

According to [Google Cloud Trace documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/manage/tracing):

### Trace Structure
Each query creates a **trace** with multiple **spans**:

1. **Root Span**: Overall request (e.g., "user asks a question")
2. **Tool Spans**: Each tool call (e.g., `web_search`, `call_code_master`)
3. **LLM Spans**: Gemini 2.5 Pro interactions
4. **Specialist Spans**: Calls to deployed Vertex AI agents
5. **Function Spans**: Individual operations within tools

### Example Trace
```
Trace: User Query "Write a Python function"
├─ LLM Span: Initial Gemini call (1.2s)
├─ Tool Span: call_code_master (3.4s)
│  └─ Vertex AI Span: CodeMaster agent (3.2s)
│     └─ LLM Span: CodeMaster's Gemini call (2.8s)
└─ LLM Span: Final response synthesis (0.8s)

Total: 5.4s
```

---

## 🌐 View Your Traces

### Option 1: Cloud Console (Recommended)
**Direct Link**: https://console.cloud.google.com/traces/list?project=studio-2416451423-f2d96

1. Go to the Trace Explorer
2. Select your project: `studio-2416451423-f2d96`
3. You'll see a Gantt chart of all requests

### Option 2: Filter Specific Traces
```
# Filter by service
service_name = "jai_cortex"

# Filter by time
time_range = "Last 1 hour"

# Filter by latency
latency > 1000ms
```

### Option 3: Search Specific Operations
```
# Find all CodeMaster calls
operation: "call_code_master"

# Find slow queries
latency > 3s

# Find errors
status: ERROR
```

---

## 🔐 Required Permissions

### Grant Cloud Trace User Role
According to [IAM documentation](https://cloud.google.com/trace/docs/iam):

```bash
# Grant yourself Cloud Trace User role
gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
    --member="user:YOUR_EMAIL@gmail.com" \
    --role="roles/cloudtrace.user"
```

**Role Capabilities**:
- ✅ View traces in Cloud Console
- ✅ List and get trace data
- ✅ Export traces to BigQuery
- ❌ Cannot modify trace configuration

---

## 📈 Export Traces to BigQuery

For long-term analysis, export traces to BigQuery per [export documentation](https://cloud.google.com/trace/docs/trace-export-bigquery):

### 1. Create BigQuery Dataset
```bash
bq mk --location=us-central1 --dataset studio-2416451423-f2d96:agent_traces
```

### 2. Enable Trace Export
```bash
gcloud logging sinks create agent-trace-sink \
    bigquery.googleapis.com/projects/studio-2416451423-f2d96/datasets/agent_traces \
    --log-filter='resource.type="cloud_trace"'
```

### 3. Query Traces in BigQuery
```sql
-- Find all CodeMaster delegations
SELECT
  timestamp,
  trace_id,
  span_name,
  duration_ms
FROM `studio-2416451423-f2d96.agent_traces.cloudtrace_*`
WHERE span_name = 'call_code_master'
ORDER BY timestamp DESC
LIMIT 100;

-- Find average response time by tool
SELECT
  span_name,
  AVG(duration_ms) as avg_duration_ms,
  COUNT(*) as call_count
FROM `studio-2416451423-f2d96.agent_traces.cloudtrace_*`
WHERE span_name LIKE 'call_%'
GROUP BY span_name
ORDER BY avg_duration_ms DESC;
```

---

## 🚨 Set Up Trace Alerts

Monitor for issues using [trace alerting](https://cloud.google.com/trace/docs/trace-alerting):

### Alert on High Latency
```yaml
# Alert if 95th percentile latency > 5 seconds
Condition: Trace span latency
Resource: cloud_trace_span
Metric: span/latency
Filter: service_name = "jai_cortex"
Threshold: 5000ms
Aggregation: 95th percentile
Duration: 5 minutes
```

### Alert on Error Rate
```yaml
# Alert if error rate > 5%
Condition: Trace span error rate
Resource: cloud_trace_span
Metric: span/error_count
Filter: service_name = "jai_cortex"
Threshold: 5%
Aggregation: Rate
Duration: 5 minutes
```

### Create Alert via Console
1. Go to **Monitoring** > **Alerting**
2. Create Policy
3. Add Condition: "Trace span"
4. Set threshold and notification channel

---

## 📝 Audit Logging

Track who accesses trace data per [audit logging docs](https://cloud.google.com/trace/docs/audit-logging):

### Enable Data Access Audit Logs
```bash
# Enable audit logging for Cloud Trace
gcloud logging settings update \
    --log-level=DATA_ACCESS \
    --log-type=cloudtrace.googleapis.com
```

### View Audit Logs
```bash
gcloud logging read \
    'protoPayload.serviceName="cloudtrace.googleapis.com"' \
    --limit 50 \
    --format json
```

### Audit Log Query Examples
```
# Who viewed traces?
protoPayload.methodName="google.devtools.cloudtrace.v2.TraceService.ListTraces"

# Who exported traces?
protoPayload.methodName="google.devtools.cloudtrace.v2.TraceService.ExportTraces"
```

---

## 🔧 Trace Data Storage & Retention

According to [trace export overview](https://cloud.google.com/trace/docs/trace-export-overview):

### Cloud Trace Retention
- **Default**: 30 days
- **Cannot be extended** in Cloud Trace itself
- **Solution**: Export to BigQuery for long-term storage

### BigQuery Storage Costs
- **Storage**: ~$0.02/GB/month
- **Queries**: ~$5/TB processed
- **Estimate**: 10,000 traces/day = ~1GB/month = $0.02/month

### Set BigQuery Table Expiration (Optional)
```bash
# Keep traces for 1 year
bq update --expiration 31536000 \
    studio-2416451423-f2d96:agent_traces.cloudtrace_*
```

---

## 🧪 Test Tracing

### Send a Test Query
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Help me write a Python function to calculate Fibonacci",
    "session_id": "trace-test-001",
    "user_id": "trace-test"
  }'
```

### Expected Trace
1. Go to Cloud Trace Explorer
2. Filter by `session_id: trace-test-001`
3. You should see:
   - Root span: chat request
   - LLM span: Gemini reasoning
   - Tool span: `call_code_master` (delegation)
   - Vertex AI span: CodeMaster agent on Vertex AI
   - LLM span: CodeMaster's Gemini call
   - Final response synthesis

---

## 📊 Trace Metrics Dashboard

Create a custom dashboard in Cloud Monitoring:

### Key Metrics to Track
1. **Request Latency**: 50th, 95th, 99th percentile
2. **Tool Call Distribution**: Which tools are used most
3. **Specialist Agent Usage**: Which specialists are called
4. **Error Rate**: Failed requests
5. **Throughput**: Requests per minute

### Sample Dashboard Widgets
```yaml
Widget 1: Latency Heatmap
  - Metric: span/latency
  - Group by: span_name
  - Visualization: Heatmap

Widget 2: Tool Call Distribution
  - Metric: span/call_count
  - Filter: span_name STARTS_WITH "call_"
  - Visualization: Pie chart

Widget 3: Error Rate
  - Metric: span/error_count
  - Calculation: Rate
  - Visualization: Line chart
```

---

## 🔗 Integration with Logs

Per [trace-log integration](https://cloud.google.com/trace/docs/trace-log-integration):

### Link Traces to Logs
Logs automatically include `trace` field when tracing is enabled:

```json
{
  "severity": "INFO",
  "message": "Called CodeMaster specialist",
  "trace": "projects/studio-2416451423-f2d96/traces/abc123...",
  "spanId": "def456...",
  "labels": {
    "tool": "call_code_master",
    "specialist": "CodeMaster"
  }
}
```

### View Logs for a Trace
1. Open trace in Cloud Trace Explorer
2. Click "View Logs" button
3. See all logs associated with that request

---

## 💰 Pricing

From [Cloud Trace pricing](https://cloud.google.com/trace/pricing):

### Free Tier
- ✅ First **2 million trace spans/month** = **FREE**
- ✅ Storage for 30 days = **FREE**

### After Free Tier
- **$0.20 per million spans** after first 2M
- **Example**: 10,000 requests/day × 5 spans each = 1.5M spans/month = **FREE**

### Estimate for Your Usage
- Assuming 1,000 queries/day
- Each query = ~5 spans (root + tools + LLM + specialists)
- Total: 150,000 spans/month = **FREE TIER** ✅

---

## ✅ Verification Checklist

After running a test query:

- [ ] Trace appears in Cloud Trace Explorer
- [ ] Can see tool calls (web_search, call_code_master, etc.)
- [ ] Can see specialist agent delegations to Vertex AI
- [ ] Can see LLM interaction spans
- [ ] Trace shows complete timeline with durations
- [ ] Can filter and search traces
- [ ] Audit logs show trace access (if enabled)
- [ ] BigQuery export working (if configured)

---

## 📚 Documentation References

- [Agent Engine Tracing](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/manage/tracing)
- [Cloud Trace Setup](https://cloud.google.com/trace/docs/setup)
- [IAM Permissions](https://cloud.google.com/trace/docs/iam)
- [Trace Alerting](https://cloud.google.com/trace/docs/trace-alerting)
- [Audit Logging](https://cloud.google.com/trace/docs/audit-logging)
- [Export to BigQuery](https://cloud.google.com/trace/docs/trace-export-bigquery)
- [Trace-Log Integration](https://cloud.google.com/trace/docs/trace-log-integration)

---

## 🎯 Next Steps

1. **Test immediately**: Send a chat request and view the trace
2. **Grant IAM role**: Give yourself Cloud Trace User access
3. **Set up BigQuery export**: For long-term trace analysis
4. **Create alerts**: Monitor for high latency or errors
5. **Build dashboard**: Visualize agent usage patterns

**Your tracing is NOW LIVE!** Every request to JAi Cortex OS is being traced. 📊

