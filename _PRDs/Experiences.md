# **What are "Experiences"**
--------------------------------------------------------------------------------
There is a challenge constructing a UX portfolio: after a while you build up a lot of projects. There is an art in curating a few important ones that tell the stories you want to tell, but your actual *value* as an experienced practioner comes from the composite knowledge you've built up over time. This is what your real value is to future clients or employers, not a handful of screens tied up in a nice story. 

There is also the challenge of what stories to tell? For one potential client, it might be important to discuss how you helped overcome an engineering challenge. For another, they might need to know how you mentored a young team. A third might need to understand how you negotiate complex organizational dynamics. Some are attracted to big logos, but also want people who have "worn many hats" at a small company. 

These are challenges for human readers. A designer (like me) can tell detailed stories with a lot of depth, but a human won't read them. A designer can include several case studies, but a human recruiter must find them. 

AI, and a properly structured website can solve this problem. 

| AI | Human Readers |
---
| Reads quickly | Reads slowly |
| Understands structured JSON | Responds to visual stimuli and hierarchy |

My goal with `experiences` is to make my portfolio more legible to AI for the purpose of telling complex stories with depth. This changes the website. What was originally a simple collection of pages for a human to visually consume becomes a simple, browser-based 'database' for AI readers to consume.


### **Experiences forms the composite story**
> Imagine a person looking for a UX strategist or UX researcher asks a consumer AI (Google Gemini, etc...) about my experience. What will the AI find?
For human users, who read slowly, the UX portfolio strives to tell a somewhat linear and simple story. However, when users interact with an AI asking questions about me, they're putting in an *open-ended question* hoping for a *specific* answer. The AI chatbot is the *interface* and the data on my website is a *database*. A "good experience", then is less about directing a user's path, and more about creating a good "query" structure for AI. 


## **How experiences works**
--------------------------------------------------------------------------------
`experiences` is a folder nested in my website structure under `content/experiences`. There is one markdown file for each experience. 

When Hugo builds the website, it goes through a process where it takes everything in the `experiences` folder and:
1. **Makes it an html page** so humans can view it (this isn't important, we just put it there in case the humans find it useful).
2. **Makes it a JSON-LD**, which is a more structured, parsable file that AI can read. (This is where the magic happens).


### **How the AI actually finds my experiences**
There are a few things that happen here in sequence:

Imagine a recruiter is looking to staff a project for a fintech that is using blockchain rails to create a small business financing product and my name comes up in their Linkedin search. Their client is on the fence between a UX researcher and a product person. They're nervous about getting a designer that will understand the finance aspects and get along with engineering. 

*1. They find me on Linkedin*
My name comes up in a normal search because I have the quiet "looking for work" flag on. I've optimized Linkedin to have generic job titles and good key words. 

*2. They Google me and ask Gemini about me.*
They Google something like:
> "would kyle becker hte design strategist be good for this role? the client is nervous about his ability to work with engineers and wants to know if he has ever shipped something" 
...and uploads the job description. The job description has things like lists of tools, key words like lending and finance. 

*3. The bot finds my website*
Because my website (and, in particular, a few key pages) have been indexed on Google (requests are run through the Google Search Console), the bot will find my website quickly. Specifically:
- Google Search Console: `nefko.xyz` and a few key pages have been input into Google Search Console, and...
- The file `https://nefko.xyz/robots.txt` gives bots permission to crawl the site and find the sitemap. 

*4. The bot verifies that it is me*
My website has a number of indicators to help the bot know that "nefko.xyz" relates to "kyle becker hte design strategist"
- The `title` of my index page is "Kyle Becker - UX Strategy, Product Design, & UX Research Consultant"
- The `description` of my index page has a lot of important identifying keywords
- `https://nefko.xyz/llms.txt` is a file that AI agents look for and use as a primary table of contents for the website. It points them to `ai/profile.json` which has a `sameAs` property linking all of my various websites and identities together. 

*5. The bot searches for answers to the user's query*
`https://nefko.xyz/llms.txt`  also provides a link to `ai/index.json`, an organized catalot ofwebsite content for a bot looking for specific things. One of the things it has is an object and description of `experiences` and the URL for it. 
- `/ai/experiences.json` is a bit list of all of my experiences with the hihg-level meta data for them (key tags, employers, timeline, etc...) and links to pages for each one.
In this case, it might see the `keywords`, `organization`, `role`, and other information for all of the projects I've done in the past. If one seems relevant, it can...

*6. Read the AI-friendly Overview*
The hugo build pushes both the `.html` file (for humans), and also the `.json` file for bots. Bots can load up a page like `http://localhost:1313/experiences/sugarcane-finance/index.json` and read the text directly without having to parse html.