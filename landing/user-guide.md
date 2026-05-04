# Contribs Mobile App User Guide

_A political contribution data aggregation mobile application_

---

## 1. Introduction

Contribs is a mobile application that aggregates and presents United States political contributions to users. Contribs is an Android-exclusive application that users can download onto their mobile device. No account creation or sign up is required — Contribs offers free and easy access to polsitical contribution data so users can see where political candidates are getting their funding from and how much.

### 1.1 Data Sources

Contribs uses imported bulk data from the official FEC (Federal Elections Commission of the USA). Currently this application has data from the 2025–2026 filing year. This data is still changing, so updates will be made at regular intervals to keep information up to date.

### 1.2 Data Definitions

A **Candidate** is someone who has either registered with the FEC or appeared on a ballot prepared by a state elections office.

An **Election** is a combination of a state, office, district, election year and party data points from the FEC. A candidate is linked to an election on our Elections page based on their state, office, district, party and election year.

A **Committee** is a political group, organization or club that spends money to influence elections or policy changes. The FEC categorizes them by who runs them — candidate committees, party committees and Political Action Committees (PACs). Some committees are linked to a specific candidate and others are not.

---

## 2. Getting Started

There is no account creation necessary to use Contribs. Contribs only displays political contribution data to a user via a simple UI with the option to "favorite" candidates and elections. This data is saved locally onto a user's device and can be found in the Profile section on the bottom navigation bar.

### 2.1 Navigation

Contribs uses a bottom navigation bar with four buttons: **Elections**, **Candidates**, **Contributions**, and **Profile**. Tapping any of these buttons takes the user directly to that section of the app.

### 2.2 Features

**Elections**
The Elections page gives users a high-level view of political activity by state and office. Users can filter the displayed data using state and office filters. The page displays the top current elections, the top 10 contributors, and the top 10 employers contributing to those elections — all sorted from highest to lowest contribution amounts.

**Candidates**
The Candidates page displays a list of all candidates currently in the database. Tapping a candidate opens their detail page with further information. Party filter chips can be used to filter candidates by party: Republican, Democrat, Independent and Other.

**Contributions**
The Contributions page displays a list of political contributions. Users can filter contributions by amount using filter chips at the top of the screen. Tapping a contribution opens a contribution detail page with more information about that contribution.

**Profile**
The Profile page stores a user's favorited candidates and elections. Favorites are saved locally on the device and do not require an account.

---

## 3. Understanding and Using Finance Data

!!! note
Contribs is currently in its early stages. Data is sourced from the FEC and reflects the 2025–2026 election cycle only. Historical data is not available at this time, and data is not yet updated on a regular basis. Real-time data sync via API is a planned future improvement.

**Candidate Detail Page**
Tapping a candidate from the Candidates page opens their detail page. This page is broken into several sections. The About section displays the candidate's office and election cycle. The Financial Summary shows the total amount the candidate has received this cycle and their leading donor. Below that, the candidate's top 5 contributors are listed. Finally, any committees associated with the candidate are displayed. Tapping a committee opens a dialogue box showing the committee's name, total amount raised, and treasurer.

**Contribution Detail Page**
Tapping a contribution from the Contributions page opens its detail page, which shows who the contribution is from, who it is to, the amount, the associated committee, and the associated candidate.

**Elections Page**
The Elections page defaults to showing the top elections overall. Using the state and office filters narrows the results to matching elections. Tapping an election from the filtered results brings the user to a list of candidates associated with that election, and tapping a candidate from that list navigates to their detail page.

---

## 4. Future Implementations

The following are features planned for future implementation.

**Real-Time Data Sync via API**
Contribs currently uses imported bulk data from the FEC that is updated at manual intervals. A future implementation would connect the app directly to the FEC API, allowing contribution data to update automatically and in real time.

**Interactive Map**
A map-based view of political contribution data is planned, allowing users to explore contributions and elections geographically across the United States.

**Location Data**
Integration of device location data would allow Contribs to automatically surface relevant elections and candidates based on where a user is located, personalizing the experience without requiring any manual input.
