#!/bin/bash
# View and analyze Cloud Traces for JAi Cortex OS

PROJECT_ID="studio-2416451423-f2d96"
LOCATION="us-central1"

echo "📊 JAi Cortex OS - Cloud Trace Viewer"
echo "======================================"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Function to open Cloud Trace Explorer
open_trace_explorer() {
    echo "🌐 Opening Cloud Trace Explorer in browser..."
    echo "URL: https://console.cloud.google.com/traces/list?project=$PROJECT_ID"
    
    # Open in default browser (macOS)
    open "https://console.cloud.google.com/traces/list?project=$PROJECT_ID" 2>/dev/null || \
    # Linux
    xdg-open "https://console.cloud.google.com/traces/list?project=$PROJECT_ID" 2>/dev/null || \
    # Windows WSL
    explorer.exe "https://console.cloud.google.com/traces/list?project=$PROJECT_ID" 2>/dev/null || \
    echo "Please open this URL manually: https://console.cloud.google.com/traces/list?project=$PROJECT_ID"
}

# Function to list recent traces
list_recent_traces() {
    echo "📋 Fetching recent traces..."
    gcloud trace list --project=$PROJECT_ID --limit=10 --format="table(traceId,startTime,duration)"
}

# Function to get trace details
get_trace_details() {
    read -p "Enter trace ID: " TRACE_ID
    echo ""
    echo "🔍 Fetching details for trace: $TRACE_ID"
    gcloud trace describe $TRACE_ID --project=$PROJECT_ID
}

# Function to check IAM permissions
check_permissions() {
    echo "🔐 Checking your Cloud Trace permissions..."
    echo ""
    
    # Get current user
    CURRENT_USER=$(gcloud config get-value account)
    echo "Current user: $CURRENT_USER"
    echo ""
    
    # Check if user has Cloud Trace User role
    POLICY=$(gcloud projects get-iam-policy $PROJECT_ID --flatten="bindings[].members" --format="table(bindings.role)" --filter="bindings.members:$CURRENT_USER")
    
    if echo "$POLICY" | grep -q "cloudtrace.user"; then
        echo "✅ You have Cloud Trace User role"
    else
        echo "❌ You DON'T have Cloud Trace User role"
        echo ""
        echo "To grant yourself access, run:"
        echo "gcloud projects add-iam-policy-binding $PROJECT_ID \\"
        echo "    --member=\"user:$CURRENT_USER\" \\"
        echo "    --role=\"roles/cloudtrace.user\""
    fi
}

# Function to export traces to BigQuery
setup_bigquery_export() {
    echo "📤 Setting up BigQuery export..."
    echo ""
    
    # Create dataset if it doesn't exist
    bq mk --location=$LOCATION --dataset $PROJECT_ID:agent_traces 2>/dev/null
    
    # Create Cloud Logging sink
    gcloud logging sinks create agent-trace-sink \
        bigquery.googleapis.com/projects/$PROJECT_ID/datasets/agent_traces \
        --log-filter='resource.type="cloud_trace"' \
        --project=$PROJECT_ID 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ BigQuery export configured"
        echo "Dataset: $PROJECT_ID:agent_traces"
    else
        echo "⚠️  Sink may already exist or you need permissions"
    fi
}

# Function to query BigQuery traces
query_bigquery_traces() {
    echo "🔍 Querying BigQuery for trace analytics..."
    echo ""
    
    # Check if bq is installed
    if ! command -v bq &> /dev/null; then
        echo "❌ bq CLI not found. Install gcloud SDK tools."
        return 1
    fi
    
    echo "Select a query:"
    echo "1. Recent traces (last 100)"
    echo "2. Tool usage distribution"
    echo "3. Average latency by tool"
    echo "4. Error rate analysis"
    read -p "Choice (1-4): " CHOICE
    
    case $CHOICE in
        1)
            bq query --use_legacy_sql=false --project_id=$PROJECT_ID "
                SELECT
                  timestamp,
                  trace_id,
                  span_name,
                  duration_ms
                FROM \`$PROJECT_ID.agent_traces.cloudtrace_*\`
                ORDER BY timestamp DESC
                LIMIT 100
            "
            ;;
        2)
            bq query --use_legacy_sql=false --project_id=$PROJECT_ID "
                SELECT
                  span_name,
                  COUNT(*) as call_count
                FROM \`$PROJECT_ID.agent_traces.cloudtrace_*\`
                WHERE span_name LIKE 'call_%'
                GROUP BY span_name
                ORDER BY call_count DESC
            "
            ;;
        3)
            bq query --use_legacy_sql=false --project_id=$PROJECT_ID "
                SELECT
                  span_name,
                  AVG(duration_ms) as avg_duration_ms,
                  MIN(duration_ms) as min_duration_ms,
                  MAX(duration_ms) as max_duration_ms,
                  COUNT(*) as call_count
                FROM \`$PROJECT_ID.agent_traces.cloudtrace_*\`
                WHERE span_name LIKE 'call_%'
                GROUP BY span_name
                ORDER BY avg_duration_ms DESC
            "
            ;;
        4)
            bq query --use_legacy_sql=false --project_id=$PROJECT_ID "
                SELECT
                  DATE(timestamp) as date,
                  COUNT(*) as total_spans,
                  COUNTIF(status = 'ERROR') as error_count,
                  SAFE_DIVIDE(COUNTIF(status = 'ERROR'), COUNT(*)) * 100 as error_rate_pct
                FROM \`$PROJECT_ID.agent_traces.cloudtrace_*\`
                GROUP BY date
                ORDER BY date DESC
                LIMIT 30
            "
            ;;
        *)
            echo "Invalid choice"
            ;;
    esac
}

# Main menu
while true; do
    echo ""
    echo "Choose an option:"
    echo "1. Open Cloud Trace Explorer (browser)"
    echo "2. List recent traces (CLI)"
    echo "3. Get trace details by ID"
    echo "4. Check IAM permissions"
    echo "5. Setup BigQuery export"
    echo "6. Query traces in BigQuery"
    echo "7. Exit"
    echo ""
    read -p "Selection (1-7): " OPTION
    
    case $OPTION in
        1)
            open_trace_explorer
            ;;
        2)
            list_recent_traces
            ;;
        3)
            get_trace_details
            ;;
        4)
            check_permissions
            ;;
        5)
            setup_bigquery_export
            ;;
        6)
            query_bigquery_traces
            ;;
        7)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid option"
            ;;
    esac
done

