---
id: 984985189456
title: Doubling first time user retention for an established notebook app
description: "A case study about how Kyle Becker, a UX strategist, worked with Rocketbook to redesign and launch a new version of its app. The app struggled with low retention for first time users. Kyle led the effort to redesign and played a product management role. They launched the new app before the company's most important retail month of the year and new user retention doubled."
subtitle: "A strategic reorienting of the Rocketbook app."
client: "Rocketbook (BIC)"
short-title: "Case Study: Rocketbook"
type: case-study
categories:
- work
featured_image: "hero.png"
tags:
- Design
- Product Management
- Quantitative Research
- Mixpanel
- Figma
- Jira 
- Visual Design
---


{{< case-study-summary >}}
Challenge: Rocketbook had strong seasonal app downloads, but many first-time users failed to complete their first scan or return after initial use.
Role: Fractional Product Manager, Designer, Design Researcher
Result: Second-month retention doubled from 30% to 60% after onboarding and key-flow improvements.
{{< /case-study-summary >}}



John Lees, a BIC executive, had a problem. Head of Rocketbook, one of the conglomerate's portfolio companies, he had been charged with revamping the product offering and finding profitability for the niche—but well-loved—brand of reusable notebooks. Part of the quandry was about the app: it had long been a part of the product offering, and downloads had always been high, but usage drop-off was steep. What was wrong with the app? How could they get people to use it?

{{< 
    figure src="./assets/photo_scan.png" 
    alt="Image of the Rocketbook app scanning a page in a Rocketbook notebook." 
    caption="Rocketbook sold reusable notebooks that came with a free app. The app enables users to scan their pages and send them, edit them, and easily send them to pre-congigured destinations. The notebooks boasted a niche group of super users, but a steep learning curve for new users." 
    >}}

That was the discussion on the first call. With the budget they had, the team had discussed hiring an agency, but they didn't want a powerpoint, *they needed someone that would work with engineering to build an app*. Hiring a junior in-house designer was off the table: to much of a management challenge and an HR headache. Their head of engineering had worked with me before in a previous role, so they reached out to me. 

{{< testimonial-block testimonial="john-lees" quote="rocketbook-case-quote" >}}

### **December or bust.**
Our timeline was also clear. As a retail personal organization product, *by far* the most imoprtant month of the year for Rocketbook was December. The month brought an influx of customers driven by both the Christmas rush and New Years' resolutions. Each year, this led to a rise in Rocketbook App downloads... and the massive crash in usage come February. The wave of customers downloaded the app in the first month, but by the second month 2/3rds hadn't opened it again. The first step in laying down a longer-term product strategy would be to try to retain these users: could we get people to keep opening the app long enough to establish a habit?

>(Spoilers: We did. We doubled retention for first time users.)

### **Strategy or implementation? Yes.**

---

The team was conflicted: they needed some short-term wins, but also a way to think longer term about the product strategy, so I put together a two-track plan. We would immediately start with a ***heuristic analysis*** to identify quick wins on the onboarding and overall usability of the app. Once that was rolling, we could take a step back and assess the broader strategic goals. With a quick contract in place I got started.

> *Commitment:*  
> **Fractional:** 25% of my time over a period of 10 months

The key for me was to quickly identify our quick wins, get ahead of the dev team on designs, establish a rhythm in our sprints, and then begin to think more broadly about how the app could fit into a larger re-think of the business as a whole. 



## **Getting our quick wins with a heuristic analysis.**

---

Some design questions take deep research. Others don't. 

In a few days I was able to turn around a quick ***heuristic analysis*** that identified several detailed aspects of the onboarding process that were likely causing drag for users in onboarding. 

> **Heuristic Analysis:**  
> Having an experienced designer look at an app to identify whether it is using best practices. Heuristic analysis is less rigorous, but can be turned around quickly, especially from a designer with a lot of experience.

{{< 
    figure src="./assets/heuristic-analysis.png" 
    alt="Images from the heuristic analysis report." 
    caption="My heuristic analysis identified several quick win areas of improvement in the app." 
    >}}


 The work also outlined some broader areas to focus on long-term: key flows, an information architecture re-vamp, and visual updates to be more consistent with the company's current brand language. 

**Setting up for Dev:** With quick-wins identified, I cleaned and organized Jira, got Figma under control and implemented a new design toolkit, and added the engineering sprint meetings to my calendar.

**Setting up for Quant User Analysis:** I also set up access to the team's ***Mixpanel*** dashboard so I could start pulling quantitative reports to get a more nuanced view of the customer drop-off. We knew they weren't sticking around long enough to log in after a month, but when *exactly* were they dropping out? I wanted to find out.

**Easy solutions first: Trim Onboarding.** With the goal of getting users to their first scan faster, we set about working on easy solutions first: stripping down the onboarging flow considerably and re-structuring the call to action for the first flow.

{{< 
    figure src="./assets/shorter-onboarding.png" 
    alt="Share-out artifact instructions in Margaret's soul file" 
    caption="Rocketbook's onboarding asked several unnecessary demographic questions of users and pushed them toward complex advanced features. We streamlined the flow to get users to complete their first scan more quickly." 
    >}}

Pulling things out of an app is quicker than putting them in, so I split out the onboarding tickets for engineering to start on. 


## **Power users or first time users? Yes.**

---

With an engineering cadence in place, it was time to shift focus to the broader structural issues. I dug deeper into the mixpanel data to see exactly where things were breaking down. 

> **Signature Experience: Scan a page in your Rocketbook Notebook and send it**  
> Rocketbook sold a combination notebook + app. To relaly understand the flow, users needed to successfully scan a page and send it to a cloud destination.

I could see that many users downloaded and logged into the app, but they *didn't even complete their first scan*. Of those who successfully scanned a page, many didn't do anything with it, they just closed the app *and never opened it again*. Only 30% of users who downloaded the app opened it again in their second mongh. By their 19th month, 95% had churned.

{{< callout-block
  eyebrow="What we learned:"
  title="Many users opened the app the first time, and opened the scanner, but never completed their first scan."
>}}

Looking at the app, it wasn't hard to see why, Rocketbook's app UI told a story about the company's history: its path from startup to acquisition was focused on a narrow band of super-power users. Keeping these users happy lead the team toward spiraling complexity as a quest for the "less clicks" meant increasing amounts of hidden automations supported by a nest of toggles and switches in settings made for nearly infinite possibilities in the core experience.

Power users continued to love the app. However, for a new user, things were opaque and baffling. 

**Our new designs focused in three areas:**

1. **An updated information architecture** that kept things more visibly organized and pushed unimportant features to the background. 
2. **A simplified key-flow** that enabled power users to access sophisticated features, but didn't force complexity of new users. 
3. **A graduated system of how-to content** so new users could start simple and gradually discover optimizations. 

The process was a careful removing of several complex features from the main flow so first time users (and users who might want a simpler, more transparent experience) would be able to scan and send more quickly.

{{< 
    figure src="./assets/streamlined-scan-flow.png" 
    alt="Walkthrough of the screens in the updated 'scan' flow for the Rocketbook app." 
    caption="Out updated flow was simpler and more transparen. Advanced features were tucked away into drawers, and core action buttons were made more prominent." 
    >}}

The core value proposition of Rocketbook was innovation and efficiency, so we *did* want users to discover advanced features over time. To introduce these features in a more progressive way, we created an "Optimize your Workflow" block on the home screen to introduce optimization features more gently and transparently.

{{< 
    figure src="./assets/progressive-learning.png" 
    alt="Image showing the home screen of the app with call to action buttons for users to learn how to use advanced features." 
    caption="Advanced features were switched off by default for first time users, and the home screen now offers tutorial explanations so users can learn about them more gently and transparently." 
    >}}



### **Future-Looking Research**
As our more structural questions, we kicked off a series of research projects that would lay the foundations for the future strategic vision of Rocketbook. 


## **A dramatic improvement of first time user retention**
We were able to launch an improved version of the Android app before our deadline (and iOS was on track to follow shortly after). Our key performance metric was new-user retention: did new users make it through their first scans? Did they come back? When we measured the data at the end of my engagement, the numbers were clear: second-month retention had doubled: jumping from 30% to 60%. A higher percentage of users were sticking with the app, and our delivery was on time to ship that improvement before Rocketbook's most important month of the year. 

{{< 
    figure src="./assets/retention-increase.png" 
    alt="Share-out artifact instructions in Margaret's soul file" 
    caption="After we launched the new app, we found twice as many users were continuing to use in their second month." 
    >}}

## **An uncertain future**
The next few months in the company proved the value of a two-track strategy. As BIC turned its focus to its core business, it re-evaluated its acquisitions—including Rocketbook. This led to a shake-up of the team and a period of marketing the company to potential buyers (it would eventually sell the company to Global Printing and Packaging (GPP)). While the far-reaching strategic research is an open question, one thing is not: improved usage. 

This is why it is so critical for project teams to think broadly while also shipping in the meantime. A north-star vision keeps us moving toward the future, but it can also be thrown off track by a shifting business landscape. A team that continuously ships small improvements *at the same time* they are contemplating a long-term strategy can lock in gains even in uncertain business environments. 