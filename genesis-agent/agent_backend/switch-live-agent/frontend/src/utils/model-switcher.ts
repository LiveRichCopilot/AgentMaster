
// Copyright 2024 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * A smart model switcher to select the appropriate Gemini model based on the task.
 */

// Define the types of tasks
export type TaskType = 'live_chat' | 'general';

// Define the model names
const LIVE_CHAT_MODEL = 'gemini-2.5-flash-preview-1028';
const GENERAL_USE_MODEL = 'gemini-2.5-pro';

/**
 * Returns the appropriate model name for a given task type.
 * @param taskType The type of task for which to get the model.
 * @returns The string name of the recommended model.
 */
export const getModelForTask = (taskType: TaskType): string => {
  switch (taskType) {
    case 'live_chat':
      return LIVE_CHAT_MODEL;
    case 'general':
      return GENERAL_USE_MODEL;
    default:
      // Default to the general use model for any unknown task types
      return GENERAL_USE_MODEL;
  }
};
