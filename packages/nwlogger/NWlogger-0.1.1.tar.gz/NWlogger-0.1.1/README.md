# coeval_logger


<!-- question
1. do we actually need to log prompt ? -> for a chatbot, the prompt is actually mostly the dialogue history
2.send to the server.
3.how's the demo looks like later ?

submit format:
 -->
 {
   "meta": {
     "app_key": "xxx",
     "session_id": "xxx",
     "model_name": "GPT-4",
     "version_tag": [
       "v1",
       "eval"
     ],
     "user": {
       "name": "xxxx",
       "gender": "male"
     },
     "total_token": 3422,
     "total_cost": 78,
     "total_duration": 3452
   },
   "conversation": [
     {
       "question": "q1",
       "prompt": "chat history  + system prompt",
       "answer": "a1",
       "token": 342,
       "duration": 32, latency !!!
    },
  ]
}
