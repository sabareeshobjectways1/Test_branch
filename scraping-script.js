const axios = require('axios');

async function scrapeAndProcessData() {
    try {
        // Configuration
        const ABSTRACT_API_KEY = '8c9b595cea01412ca697b4b2bfb29246';
        const GEMINI_API_KEY = 'AIzaSyCRjKocESVskmlfPfwXwSh9vvEBxKoVzLI';
        const TARGET_URL = 'https://dealofthedayindia.com';
        
        // Step 1: Scrape the website using Abstract API
        console.log('Scraping website...');
        const scrapeResponse = await axios.get(`https://scrape.abstractapi.com/v1/`, {
            params: {
                api_key: ABSTRACT_API_KEY,
                url: TARGET_URL
            }
        });

        // Step 2: Prepare the prompt for Gemini
        const prompt = `This is the data im scraped from the website I need is to generate a single json for the product contains offers with title description offer price details generate a json file`;

        // Step 3: Call Gemini API
        console.log('Processing with Gemini AI...');
        const geminiResponse = await axios.post(
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
            {
                contents: [{
                    parts: [{
                        text: `${prompt}\n\nHTML Content:\n${scrapeResponse.data}`
                    }]
                }]
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${GEMINI_API_KEY}`
                }
            }
        );

        // Step 4: Process and format the response
        const aiResponse = geminiResponse.data.candidates[0].content.parts[0].text;
        
        // Try to parse the response as JSON
        try {
            const jsonResponse = JSON.parse(aiResponse);
            console.log('Processed JSON output:', JSON.stringify(jsonResponse, null, 2));
            return jsonResponse;
        } catch (e) {
            console.log('Raw AI response:', aiResponse);
            return aiResponse;
        }

    } catch (error) {
        console.error('Error occurred:', error.message);
        if (error.response) {
            console.error('API response error:', error.response.data);
        }
        throw error;
    }
}

// Execute the function
scrapeAndProcessData()
    .then(result => {
        console.log('Process completed successfully');
    })
    .catch(error => {
        console.error('Process failed:', error);
    });
