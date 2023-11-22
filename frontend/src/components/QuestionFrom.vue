<template>
    <div class="md:w-auto p-3 md:h-full flex flex-col gap-6  sm:w-full">
        <!-- hero title named 'Virtual mentor' -->
        <div class="w-full md:my-auto">
            <div class="w-full h-full flex justify-center items-center">
                <h1 class="text-3xl text-white">Virtual Mentor</h1>
            </div>
        </div>
        <div class="w-full h-full md:flex-1 mt-auto bg-slate-800 md:p-2 sm:px-0 md:px-10  rounded-md mb-0 md:mb-10">
            <div class="w-full md:h-full flex justify-center">
                <form class="w-full px-2" @submit.prevent="handleSubmit">
                    <div class="mb-4 w-full sm:h-auto md:h-[90%]">
                        <label for="questioninput" class="block mb-2 font-bold text-white">What is your question?</label>
                        <textarea
                            class="w-full h-full px-3 py-2 leading-tight text-white border rounded shadow appearance-none focus:outline-none focus:shadow-outline dark:bg-slate-900"
                            rows="5" v-model="question" required></textarea>
                    </div>
                    <div class="md:my-9">
                        <button type="submit" class="text-black px-4 py-2 font-bold text-white bg-blue-300 rounded hover:bg-blue-700"
                            :disabled="loading">
                            {{ loading ? 'Loading' : 'Submit' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <!--text display area which have width of 75% of parent and 100vh height -->
    <div class="flex-1 flex h-full p-4 sm:p-4 md:p-14">
        <div class="w-full h-[100%] mt-3 bg-slate-800 overflow-y-scroll text-white p-4 rounded-md" v-html="toMarkdown(streamResponse)" ></div>
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
  