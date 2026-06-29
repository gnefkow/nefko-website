---
id: 984985189456
title: Doubling first time user retention for an established notebook app
description: "A case study about how Kyle Becker, a UX strategist, worked with Rocketbook to redesign and launch a new version of its app. The app struggled with low retention for first time users. Kyle led the effort to redesign and played a product management role. They launched the new app before the company's most important retail month of the year and new user retention doubled."
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



John Lees, the head of Rocketbook had a problem: people were downloading the app, but not using it... and nobody knew why. The company—part of BIC's portfolio of acquisitions—offered a reusable notebook along with a free app. The product was straight forward: take notes on your physical notebook, scan it with the app, then wipe the notebook clean. Lees had a host of improvements in mind to improve the business,—including an app re-vamp—but first things first: how can we get people to use the app? 

{{< quote-block testimonial="john-lees" quote="rocketbook-case-quote" >}}

> Rocketbook: Reusable notebooks with an app that enables users to scan and store. A number of "smart" features help power users quickly and efficiently scan their notebooks. 

That was our discussion on the first call. With the budget they had, the team had discussed hiring an agency, but they didn't want a powerpoint deliverable. They discussed hiring a junior designer, but then they'd need to manage them (and it would take time to get through the HR process at a large company). When their head of engineering (and former collaborator of mine) Chris suggested a contractor, they reached out to me. 

Our timeline was also clear. Typical for retail products, *by far* the most imoprtant month of the year for Rocketbook was December: an influx of customers driven by both the Christmas rush, and (as a productivity product) the preperation for a fresh start on New Years' resolutions to "get organized." This mapped perfectly to the massive rise in Rocketbook App downloads... and the massive crash in usage come February. Could we improve the app in time to alter the wave?

>(Spoilers: We did. We doubled retention for first time users.)

### **Strategy or implementation? Yes.**

---

The team explained that they were conflicted: they needed some short-term wins, but also a way to think longer term about the product strategy. Would we be able to balance it all at once? I put together a two-track plan. We would immediately start with a heuristic analysis to identify quick wins on the onboarding and overall usability of the app. Once that was rolling, we could take a step back and assess the broader strategic goals. With a quick contract in place I got started.

> Commitment type: Fractional → 25% of my time over a period of 10 months

The key for me was to quickly identify our quick wins, get ahead of the dev team on designs, establish a rhythm in our sprints, and then begin to think more broadly about how the app could fit into a larger re-think of the business as a whole. 



### **Getting our quick wins with a heuristic analysis.**

---

Some design questions take deep research. Others don't. 

In a few days I was able to turn around a quick *heuristic analysis* that identified several detailed aspects of the onboarding process that were likely causing drag for users in onboarding. 

> Heuristic Analysis: having an experienced designer look at an app to identify whether it is using best practices. Heuristic analysis is less rigorous, but can be turned around quickly, especially from a designer with a lot of experience.

{{< 
    figure src="./assets/heuristic-analysis.png" 
    alt="Images from the heuristic analysis report." 
    caption="My heuristic analysis identified several quick win areas of improvement in the app." 
    >}}


 The work also outlined some broader areas to focus on long-term: key flows, an information architecture re-vamp, and visual updates to be more consistent with the company's current brand language. 

With our quick-wins identified, I got started with a Jira clean-out and started working with the engineering team on the simple stuff. (As with most clients, Figma was also a bit of a disaster, so I worked with the team to get it organized cleaner hand-offs). I also set up access to the team's Mixpanel dashboard so I could start pulling quantitative reports to get a more nuanced view of the customer drop-off. 

{{< 
    figure src="./assets/shorter-onboarding.png" 
    alt="Share-out artifact instructions in Margaret's soul file" 
    caption="Rocketbook's onboarding asked several unnecessary demographic questions of users and pushed them toward complex advanced features. We streamlined the flow to get users to complete their first scan more quickly." 
    >}}

With the goal of getting users to their first scan faster, we set about working on easy solutions first: stripping down the onboarging flow considerably and re-structuring the call to action for the first flow.


### **Power users or first time users? Yes.**

---

With an engineering cadence in place, it was time to shift focus to the broader structural issues. I dug deeper into the mixpanel data to see exactly where things were breaking down. I could see that many users didn't even complete their first scan with the app. Many who did might scan, but never do anything with the scan. By month two, only 30% of users even opened the app again, and 95% of users had churned by month 12.

{{< callout-block
  eyebrow="What we learned:"
  title="Many users opened the app the first time, and opened the scanner, but never completed their first scan."
>}}

Looking at the app, it wasn't hard to see why. Rocketbook's core business challenge was evident in its interface: the company wanted to grow its customer base, but its path from startup to acquisition was focused on a narrow band of super-power users. 

The core of the app experience was scanning: users loved their Rocketbook notebooks, and keeping these users happy lead the team toward spiraling complexity as a nest of toggles and switches in settings made for nearly infinite possibilities in the core experience. A quest for the "least clicks" for power users had led the team toward an impossible cliff for new users. 

Our new designs focused in three areas:

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