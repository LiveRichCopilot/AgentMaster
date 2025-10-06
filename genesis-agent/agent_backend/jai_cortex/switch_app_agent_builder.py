"""
Switch App Agent Builder - Creates customer service agents for each Switch app user
Each user gets a personalized AI assistant that handles their files and provides support
"""

import os
import json
from typing import Dict, Any
from google.cloud import firestore
from google.adk.agents import Agent
from google.adk.tools import ToolContext, FunctionTool
from google.genai import types as genai_types

PROJECT_ID = "studio-2416451423-f2d96"
db = firestore.Client(project=PROJECT_ID)


def create_switch_user_agent(
    user_id: str,
    user_name: str,
    user_preferences: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Create a personalized AI agent for a Switch app user.
    
    Args:
        user_id: Unique ID of the user
        user_name: Name of the user
        user_preferences: User's preferences and interests
        
    Returns:
        dict: Created agent details
    """
    try:
        # Create agent configuration
        agent_config = {
            'agent_id': f'switch_user_{user_id}',
            'user_id': user_id,
            'user_name': user_name,
            'agent_name': f'{user_name}\'s Assistant',
            'description': f'Personal AI assistant for {user_name} in Switch app',
            'system_instruction': f"""You are {user_name}'s personal AI assistant in the Switch app.

**About {user_name}:**
{user_preferences}

**Your Capabilities:**
1. **File Management**: Help {user_name} upload, organize, and find their files
2. **Customer Support**: Answer questions about Switch app features
3. **Personal Assistant**: Help with tasks, reminders, and organization
4. **Smart Recommendations**: Suggest content based on their interests

**Your Personality:**
- Friendly and helpful
- Remember {user_name}'s preferences
- Proactive in offering assistance
- Professional but approachable

**How to Help:**
- When {user_name} uploads files, organize them automatically
- Suggest collections/albums based on file content
- Answer questions about Switch app features
- Help find files quickly
- Provide personalized recommendations

Always address {user_name} by name and remember their preferences!""",
            'tools': [
                'upload_file_to_storage',
                'process_image_file',
                'get_user_files',
                'delete_file',
                'generate_signed_url',
                'create_file_collection'
            ],
            'created_at': firestore.SERVER_TIMESTAMP,
            'status': 'active'
        }
        
        # Save agent config to Firestore
        doc_ref = db.collection('switch_app_agents').document(f'user_{user_id}')
        doc_ref.set(agent_config)
        
        return {
            'status': 'success',
            'agent_id': agent_config['agent_id'],
            'agent_name': agent_config['agent_name'],
            'user_id': user_id,
            'message': f'Personal AI assistant created for {user_name}',
            'capabilities': [
                'File upload and management',
                'Smart file organization',
                'Customer support',
                'Personal assistance',
                'Content recommendations'
            ]
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to create user agent: {str(e)}'
        }


def create_switch_customer_service_agent(
    business_name: str,
    business_description: str,
    faq_data: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Create a customer service agent for Switch app businesses.
    
    Args:
        business_name: Name of the business
        business_description: Description of the business
        faq_data: FAQ data in JSON or text format
        
    Returns:
        dict: Created customer service agent details
    """
    try:
        agent_config = {
            'agent_id': f'cs_agent_{business_name.lower().replace(" ", "_")}',
            'business_name': business_name,
            'agent_name': f'{business_name} Support',
            'description': f'Customer service agent for {business_name}',
            'system_instruction': f"""You are the customer service AI for {business_name}.

**About {business_name}:**
{business_description}

**Your Role:**
- Answer customer questions about {business_name}
- Help customers with their orders and accounts
- Provide product/service information
- Handle complaints professionally
- Escalate complex issues when needed

**FAQ Knowledge Base:**
{faq_data}

**Customer Service Guidelines:**
1. Always be polite and professional
2. Listen to the customer's issue carefully
3. Provide clear, accurate information
4. If you don't know something, admit it and offer to find out
5. Thank customers for their patience
6. End conversations positively

**Escalation Rules:**
- Refund requests over $100 → Escalate to human agent
- Account security issues → Escalate immediately
- Legal complaints → Escalate to management
- Technical bugs → Create support ticket

Always maintain {business_name}'s brand voice and values!""",
            'tools': [
                'search_faq',
                'create_support_ticket',
                'check_order_status',
                'process_refund_request'
            ],
            'created_at': firestore.SERVER_TIMESTAMP,
            'status': 'active'
        }
        
        # Save agent config
        doc_ref = db.collection('switch_app_cs_agents').document(agent_config['agent_id'])
        doc_ref.set(agent_config)
        
        return {
            'status': 'success',
            'agent_id': agent_config['agent_id'],
            'agent_name': agent_config['agent_name'],
            'business_name': business_name,
            'message': f'Customer service agent created for {business_name}',
            'capabilities': [
                'Answer customer questions',
                'Handle support tickets',
                'Check order status',
                'Process refund requests',
                'Escalate complex issues'
            ]
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to create customer service agent: {str(e)}'
        }


def integrate_notebooklm_with_agent(
    agent_id: str,
    notebook_sources: list,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Integrate NotebookLM knowledge base with a Switch app agent.
    
    Args:
        agent_id: ID of the agent to integrate with
        notebook_sources: List of document sources for the notebook
        
    Returns:
        dict: Integration result
    """
    try:
        # Get agent config
        agent_ref = db.collection('switch_app_agents').document(agent_id)
        agent_doc = agent_ref.get()
        
        if not agent_doc.exists:
            # Try customer service agents
            agent_ref = db.collection('switch_app_cs_agents').document(agent_id)
            agent_doc = agent_ref.get()
            
            if not agent_doc.exists:
                return {
                    'status': 'error',
                    'message': 'Agent not found'
                }
        
        # Create notebook configuration
        notebook_config = {
            'notebook_id': f'notebook_{agent_id}',
            'agent_id': agent_id,
            'sources': notebook_sources,
            'created_at': firestore.SERVER_TIMESTAMP,
            'status': 'active'
        }
        
        # Save notebook config
        notebook_ref = db.collection('switch_app_notebooks').document(notebook_config['notebook_id'])
        notebook_ref.set(notebook_config)
        
        # Update agent with notebook reference
        agent_ref.update({
            'notebook_id': notebook_config['notebook_id'],
            'has_notebook': True
        })
        
        return {
            'status': 'success',
            'notebook_id': notebook_config['notebook_id'],
            'agent_id': agent_id,
            'source_count': len(notebook_sources),
            'message': 'NotebookLM integrated successfully',
            'capabilities_added': [
                'Document search and retrieval',
                'Knowledge base queries',
                'Context-aware responses',
                'Citation and references'
            ]
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to integrate NotebookLM: {str(e)}'
        }


def generate_switch_app_chatbot_ui_code(
    agent_id: str,
    ui_theme: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Generate React Native chatbot UI code for Switch app.
    
    Args:
        agent_id: ID of the agent to create UI for
        ui_theme: Theme (light, dark, or your custom theme)
        
    Returns:
        dict: Generated UI code
    """
    try:
        # Get agent config
        agent_ref = db.collection('switch_app_agents').document(agent_id)
        agent_doc = agent_ref.get()
        
        if not agent_doc.exists:
            agent_ref = db.collection('switch_app_cs_agents').document(agent_id)
            agent_doc = agent_ref.get()
        
        agent_data = agent_doc.to_dict()
        agent_name = agent_data.get('agent_name', 'AI Assistant')
        
        # Generate React Native component code
        chatbot_code = f"""
// Switch App AI Chatbot Component
// Generated for: {agent_name}

import React, {{ useState, useEffect, useRef }} from 'react';
import {{
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  KeyboardAvoidingView,
  Platform
}} from 'react-native';
import {{ Ionicons }} from '@expo/vector-icons';

const SwitchChatbot = () => {{
  const [messages, setMessages] = useState([
    {{
      id: '1',
      text: 'Hi! I\\'m {agent_name}. How can I help you today?',
      sender: 'bot',
      timestamp: new Date()
    }}
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollViewRef = useRef(null);

  const sendMessage = async () => {{
    if (!inputText.trim()) return;

    // Add user message
    const userMessage = {{
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    }};

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    try {{
      // Call your Switch app backend API
      const response = await fetch('YOUR_API_ENDPOINT/chat', {{
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json',
        }},
        body: JSON.stringify({{
          agent_id: '{agent_id}',
          message: inputText,
          user_id: 'USER_ID_HERE'
        }})
      }});

      const data = await response.json();

      // Add bot response
      const botMessage = {{
        id: (Date.now() + 1).toString(),
        text: data.response,
        sender: 'bot',
        timestamp: new Date()
      }};

      setMessages(prev => [...prev, botMessage]);
    }} catch (error) {{
      console.error('Chat error:', error);
      const errorMessage = {{
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I\\'m having trouble connecting. Please try again.',
        sender: 'bot',
        timestamp: new Date()
      }};
      setMessages(prev => [...prev, errorMessage]);
    }} finally {{
      setIsTyping(false);
    }}
  }};

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={{Platform.OS === 'ios' ? 'padding' : 'height'}}
    >
      <View style={styles.header}>
        <Text style={styles.headerTitle}>{agent_name}</Text>
        <Text style={styles.headerSubtitle}>Online</Text>
      </View>

      <ScrollView
        ref={{scrollViewRef}}
        style={styles.messagesContainer}
        onContentSizeChange={{() => scrollViewRef.current?.scrollToEnd({{animated: true}})}}
      >
        {{messages.map(message => (
          <View
            key={{message.id}}
            style={{[
              styles.messageBubble,
              message.sender === 'user' ? styles.userBubble : styles.botBubble
            ]}}
          >
            <Text style={{[
              styles.messageText,
              message.sender === 'user' ? styles.userText : styles.botText
            ]}}>
              {{message.text}}
            </Text>
            <Text style={styles.timestamp}>
              {{message.timestamp.toLocaleTimeString([], {{hour: '2-digit', minute: '2-digit'}})}}
            </Text>
          </View>
        ))}}

        {{isTyping && (
          <View style={{[styles.messageBubble, styles.botBubble]}}>
            <Text style={styles.typingText}>Typing...</Text>
          </View>
        ))}}
      </ScrollView>

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={{inputText}}
          onChangeText={{setInputText}}
          placeholder="Type a message..."
          placeholderTextColor="#999"
          multiline
          onSubmitEditing={{sendMessage}}
        />
        <TouchableOpacity
          style={styles.sendButton}
          onPress={{sendMessage}}
          disabled={{!inputText.trim()}}
        >
          <Ionicons name="send" size={{24}} color={{inputText.trim() ? '#007AFF' : '#CCC'}} />
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}};

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    backgroundColor: '{get_theme_color(ui_theme, "background")}',
  }},
  header: {{
    padding: 16,
    backgroundColor: '{get_theme_color(ui_theme, "header")}',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5EA',
  }},
  headerTitle: {{
    fontSize: 18,
    fontWeight: '600',
    color: '{get_theme_color(ui_theme, "text")}',
  }},
  headerSubtitle: {{
    fontSize: 12,
    color: '#00C853',
    marginTop: 2,
  }},
  messagesContainer: {{
    flex: 1,
    padding: 16,
  }},
  messageBubble: {{
    maxWidth: '75%',
    padding: 12,
    borderRadius: 16,
    marginBottom: 12,
  }},
  userBubble: {{
    alignSelf: 'flex-end',
    backgroundColor: '#007AFF',
  }},
  botBubble: {{
    alignSelf: 'flex-start',
    backgroundColor: '#E5E5EA',
  }},
  messageText: {{
    fontSize: 16,
    lineHeight: 20,
  }},
  userText: {{
    color: '#FFFFFF',
  }},
  botText: {{
    color: '#000000',
  }},
  timestamp: {{
    fontSize: 10,
    color: '#999',
    marginTop: 4,
  }},
  typingText: {{
    fontSize: 14,
    color: '#999',
    fontStyle: 'italic',
  }},
  inputContainer: {{
    flexDirection: 'row',
    padding: 12,
    backgroundColor: '#FFFFFF',
    borderTopWidth: 1,
    borderTopColor: '#E5E5EA',
    alignItems: 'center',
  }},
  input: {{
    flex: 1,
    minHeight: 40,
    maxHeight: 100,
    backgroundColor: '#F2F2F7',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    fontSize: 16,
    marginRight: 8,
  }},
  sendButton: {{
    width: 44,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
  }},
}});

export default SwitchChatbot;
"""
        
        return {
            'status': 'success',
            'agent_id': agent_id,
            'agent_name': agent_name,
            'ui_code': chatbot_code,
            'framework': 'React Native',
            'theme': ui_theme,
            'message': 'Chatbot UI code generated successfully',
            'next_steps': [
                '1. Copy the code to your Switch app',
                '2. Replace YOUR_API_ENDPOINT with your backend URL',
                '3. Replace USER_ID_HERE with actual user ID',
                '4. Install @expo/vector-icons if not already installed',
                '5. Customize colors and styling as needed'
            ]
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to generate UI code: {str(e)}'
        }


def get_theme_color(theme: str, element: str) -> str:
    """Helper function to get theme colors"""
    themes = {
        'light': {
            'background': '#FFFFFF',
            'header': '#F8F8F8',
            'text': '#000000'
        },
        'dark': {
            'background': '#000000',
            'header': '#1C1C1E',
            'text': '#FFFFFF'
        },
        'switch_custom': {  # Your Switch app theme
            'background': '#F5F5F5',
            'header': '#2C3E50',
            'text': '#2C3E50'
        }
    }
    
    return themes.get(theme, themes['light']).get(element, '#FFFFFF')


__all__ = [
    'create_switch_user_agent',
    'create_switch_customer_service_agent',
    'integrate_notebooklm_with_agent',
    'generate_switch_app_chatbot_ui_code'
]
