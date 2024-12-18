* test case 1
    * 설정  
        --max_memory 48
        --max_length 32768 
        --max_new_tokens 1024 

        device: self.model.device
        stream: False

    * 답변 소요 시간: 5m 48s

* test case 2
    * 설정  
        --max_memory 48
        --max_length 32768 
        --max_new_tokens 1024 

        device: mps
        stream: False

    * 답변 소요 시간: 1m 15s 2m 27s, 30s

* test case 3
    * 설정  
        --max_memory 48
        --max_length 4096 
        --max_new_tokens 1024 

        device: mps
        stream: False

    * 답변 소요 시간: 50s, 1m, 41.7s

* test case 3
    * 설정  
        --max_memory 48
        --max_length 2048 
        --max_new_tokens 1024 

        device: mps
        stream: False

    * 답변 소요 시간: 50s

* test case 3
    * 설정  
        --max_memory 48
        --max_length 1024
        --max_new_tokens 1024 

        device: mps
        stream: False

    * 답변 소요 시간: 60s, 38s, 37s