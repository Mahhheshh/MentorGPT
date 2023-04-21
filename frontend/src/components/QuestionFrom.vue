<template>
    <div class="w-1/4 h-screen">
        <!-- hero title named 'Virtual mentor' -->
        <div class="w-full h-1/6">
            <div class="w-full h-full flex justify-center items-center">
                <h1 class="text-3xl text-white">Virtual Mentor</h1>
            </div>
        </div>
        <div class="w-full h-3/4">
            <div class="w-full h-full flex justify-center">
                <form @submit.prevent="handleSubmit">
                    <div class="mb-4 w-full h-5/6">
                        <label for="questioninput" class="block mb-2 font-bold text-white">What is your question?</label>
                        <textarea
                            class="w-full h-full px-3 py-2 leading-tight text-white border rounded shadow appearance-none focus:outline-none focus:shadow-outline dark:bg-gray-800"
                            rows="5" v-model="question" required></textarea>
                    </div>
                    <div class="my-9">
                        <button type="submit" class="px-4 py-2 font-bold text-white bg-blue-500 rounded hover:bg-blue-700"
                            :disabled="loading">
                            {{ loading ? 'Loading' : 'Submit' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <!--text display area which have width of 75% of parent and 100vh height -->
    <div class="w-3/4 h-screen">
        <div class="w-full h-full" v-html="toMarkdown(streamResponse)" style="margin-top: 55px;"></div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent, ref } from 'vue';
import MarkdownIt from 'markdown-it';

interface ResponseChunk {
    value?: ArrayBuffer;
    done: boolean;
}

export default defineComponent({
    setup() {
        const question = ref('');
        const loading = ref(false);
        // const airesponse = ref('');
        const streamResponse = ref('');

        const handleSubmit = async () => {
            loading.value = true; // show the loading spinner
            streamResponse.value = ''; // reset the stream response

            try {
                const response = await fetch('http://127.0.0.1:5000/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        question: question.value,
                    })
                });

                // check if the response is ok

                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }

                // get the response body
                const reader = response.body?.getReader();

                // check if the response body is null
                if (!reader) {
                    throw new Error('Response body is null');
                }

                // read the response body
                let result: ResponseChunk;
                let responseData = '';
                let word = '';
                do {
                    result = await reader.read();
                    if (result.value) {
                        const decoder = new TextDecoder();
                        const text = decoder.decode(result.value, { stream: true });
                        const words = text.split(' ');
                        for (let i = 0; i < words.length; i++) {
                            word += words[i];
                            if (i !== words.length - 1) {
                                streamResponse.value += word + ' ';
                                word = '';
                            }
                        }
                    }
                    responseData += word;
                } while (!result.done);
                if (word !== '') {
                    streamResponse.value += word;
                }
                // airesponse.value = responseData;
            } catch (error) {
                console.log(error);
                // airesponse.value = 'Something went wrong';
                streamResponse.value = 'Something went wrong';
            } finally {
                loading.value = false;
                // console.log(airesponse);
            }
        };

        const toMarkdown = (text: string) => {
            const md = new MarkdownIt();
            return md.render(text);
        };

        return {
            question,
            loading,
            streamResponse,
            handleSubmit,
            toMarkdown,
        };
    }
});
</script>
  