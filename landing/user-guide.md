# 

# Contribs Mobile App User Guide

*A political contribution data aggregation application*  
*![][image1]*  
---

1. ### Introduction

   Contribs is a mobile application that aggregates and presents United States political contributions to users. Contribs is an Android-exclusive application that users can download onto their mobile device. No account creation or sign up is required, Contribs offers free and easy access to political contribution data so users can see where political candidates are getting their funding from and how much. 

#### 1.1 Data Sources

Contribs uses imported bulk data from the official FEC (Federal Elections Commission of the USA). Currently this application has data from the 2025-2026 filing year. This data is still changing, so updates will be made at regular intervals to keep information up to date. 

#### 1.2 Data Definitions

A “**Candidate**” is someone who has either registered with the FEC or appeared on a ballot listed prepared by a state elections office. 

An “**Election**” is a combination of a state, office, district, election year and party data points from the FEC. A candidate is linked to an election on our Elections page based on their state, office, district, party and election year. 

A “**Committee**” is a political group, organization or club that spends money to influence elections or policy changes. The FEC categorizes them by who runs them i.e. candidate committees, party committees and Political Action Committees (PACs). Some committees are linked to a specific candidate and others are not.   
---

2. ### Getting Started

   There is no account creation necessary to use contribs. Contribs only displays political contribution data to a user via a simple UI with the option to “favorite” candidates and elections. This data is saved locally onto a user's device and can be found in the “profile” section on the bottom navigation bar. 

   #### 2.1 Navigation

   Contribs uses a bottom navigation bar with four buttons: Elections, Candidates, Contributions, and Profile. Tapping any of these buttons takes the user directly to that section of the app.

   #### 2.2 Features

   **Elections** The Elections page gives users a high-level view of political activity by state and office. Users can filter the displayed data using state and office filters. The page displays the top current elections, the top 10 contributors, and the top 10 employers contributing to those elections. All sorted from highest to lowest contribution amounts.   
   **Candidates** The Candidates page displays a list of all candidates currently in the database. Tapping a candidate opens their detail page with further information. Party filter chips can be used to filter candidates by party: Republican, Democrat, Independent and Other.   
   **Contributions** The Contributions page displays a list of political contributions. Users can filter contributions by amount using filter chips at the top of the screen. Tapping a contribution opens a contribution detail page with more information about that contribution.  
   **Profile** The Profile page stores a user's “favorited” candidates and elections. Favorites are saved locally on the device and do not require an account.

---

3. ### Understanding and Using Finance Data

   ***Note:** Contribs is currently in beta. Data is sourced from the FEC and reflects the 2025–2026 election cycle only. Historical data is not available at this time, and data is not yet updated on a regular basis. Real-time data sync via API is a planned future improvement.*  
   **Candidate Detail Page** Tapping a candidate from the Candidates page opens their detail page. This page is broken into several sections. The About section displays the candidate's office and election cycle. The Financial Summary shows the total amount the candidate has received this cycle and their leading donor. Below that, the candidate's top 5 contributors are listed. Finally, any committees associated with the candidate are displayed. Tapping a committee opens a dialogue box showing the committee's name, total amount raised, and treasurer.  
   **Contribution Detail Page** Tapping a contribution from the Contributions page opens its detail page, which shows who the contribution is from, who it is to, the amount, the associated committee, and the associated candidate.  
   **Elections Page** The Elections page defaults to showing the top elections overall. Using the state and office filters narrows the results to matching elections. Tapping an election from the filtered results brings the user to a list of candidates associated with that election, and tapping a candidate from that list navigates to their detail page.

---

4. ### App Screenshots

---

5. ### Future Implementations

   *The following are future features that would have been considered for implementation*

   

   **Real-Time Data Sync via API:** Contribs currently uses imported bulk data from the FEC that is theoretically updated at manual intervals. A future implementation would connect the app directly to the FEC API, allowing contribution data to update automatically and in real time.

   

   **Interactive Map:** A map-based view of political contribution data is planned, allowing users to explore contributions and elections geographically across the United States.

   

   **Location Data:** Integration of device location data would allow Contribs to automatically surface relevant elections and candidates based on where a user is located, personalizing the experience without requiring any manual input.

[image1]: <data:image/png;base64,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>