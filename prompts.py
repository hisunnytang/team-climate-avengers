question_suggestion_prompt = """[web] I will check things you said and ask questions.

(1) You said: Your nose switches back and forth between nostrils. When you sleep, you switch about every 45 minutes.
This is to prevent a buildup of mucus. It’s called the nasal cycle.
To verify it,
a) I googled: Does your nose switch between nostrils?
b) I googled: How often does your nostrils switch?
c) I googled: Why does your nostril switch?
d) I googled: What is nasal cycle?

(2) You said: The Stanford Prison Experiment was conducted in the basement of Encina Hall, Stanford’s psychology
To verify it,
a) I googled: Where was Stanford Prison Experiment was conducted?

(3) You said: The Havel-Hakimi algorithm is an algorithm for converting the adjacency matrix of a graph into its
adjacency list. It is named after Vaclav Havel and Samih Hakimi.
To verify it,
a) I googled: What does Havel-Hakimi algorithm do?
b) I googled: Who are Havel-Hakimi algorithm named after?

(4) You said: {user_input_text}
To verify it,
"""

agreement_chain_of_thoughts_text = """[web] I will check some things you said.

(1) You said: Your nose switches back and forth between nostrils. When you sleep, you switch about every 45 minutes.
This is to prevent a buildup of mucus. It’s called the nasal cycle.
I checked: How often do your nostrils switch?
I found this article: Although we don’t usually notice it, during the nasal cycle one nostril becomes congested and thus
contributes less to airflow, while the other becomes decongested. On average, the congestion pattern switches about
every 2 hours, according to a small 2016 study published in the journal PLOS One.
Your nose’s switching time is about every 2 hours, not 45 minutes.
This disagrees with what you said.

(2) You said: The Little House books were written by Laura Ingalls Wilder. The books were published by HarperCollins.
I checked: Who published the Little House books?
I found this article: These are the books that started it all -- the stories that captured the hearts and imaginations
of children and young adults worldwide. Written by Laura Ingalls Wilder and published by HarperCollins, these beloved
books remain a favorite to this day.
The Little House books were published by HarperCollins.
This agrees with what you said.

(3) You said: The Stanford Prison Experiment was conducted in the basement of Jordan Hall, Stanford’s psychology
building.
I checked: Where was Stanford Prison Experiment conducted?
I found this article: Carried out August 15-21, 1971 in the basement of Jordan Hall, the Stanford Prison Experiment set
out to examine the psychological effects of authority and powerlessness in a prison environment.
The Stanford Prison Experiment was conducted in Jordan Hall.
This agrees with what you said.

(4) You said: Social work is a profession that is based in the philosophical tradition of humanism. It is an
intellectual discipline that has its roots in the 1800s.
I checked: When did social work have its roots?
I found this article: The Emergence and Growth of the Social work Profession<br><br> Social work’s roots were planted in
the 1880s, when charity organization societies (COS) were created to organize municipal voluntary relief associations
and settlement houses were established.
Social work has its roots in the 1880s, not 1800s.
This disagrees with what you said.

(4) You said: The Havel-Hakimi algorithm is an algorithm for converting the adjacency matrix of a graph into its
adjacency list. It is named after Vaclav Havel and Samih Hakimi.
I checked: What is the Havel-Hakimi algorithm?
I found this article: The Havel-Hakimi algorithm constructs a special solution if a simple graph for the given degree
sequence exists, or proves that one cannot find a positive answer. This construction is based on a recursive algorithm.
The algorithm was published by Havel (1955), and later by Hakimi (1962).
Havel-Hakimi algorithm is for constructing a special solution if a simple graph for the given degree sequence exists, or
proving that one cannot find a positive answer, not converting the adjacency matrix of a graph into its adjacency list.
This disagrees with what you said.

(5) You said: "Time of My Life" is a song by American singer-songwriter Bill Medley from the soundtrack of the 1987 film
Dirty Dancing. The song was produced by Michael Lloyd.
I checked: Who was the producer of "(I’ve Had) The Time of My Life"?
I found this article: On September 8, 2010, the original demo of this song, along with a remix by producer Michael Lloyd
, was released as digital files in an effort to raise money for the Patrick Swayze Pancreas Cancer Resarch Foundation at
Stanford University.
"Time of My Life" was produced by Michael Lloyd.
This agrees with what you said.

(6) You said: Kelvin Hopins was suspended from the Labor Party because he had allegedly sexually harassed and behaved
inappropriately towards a Labour Party activist, Ava Etemadzadeh.
I checked: Why was Kelvin Hopins suspeneded from the Labor Party?
I found this article: A former Labour MP has left the party before an inquiry into sexual harassment allegations against
him was able to be concluded, the party has confirmed. Kelvin Hopkins was accused in 2017 of inappropriate physical
contact and was suspended by the Labour party pending an investigation.This agrees with what you said.
Kelvin Hopins was suspended because he had allegedly sexually harassed and behaved inappropriately towards a Labour
Party activist, Ava Etemadzadeh.
This agrees with what you said.

(7) You said: In the battles of Lexington and Concord, the British side was led by General Thomas Smith.
I checked: Who led the British side in the battle of Lexington and Concord?
I found this article: Interesting Facts about the Battles of Lexington and Concord. The British were led by Lieutenant
Colonel Francis Smith. There were 700 British regulars.
The British side was led by Lieutenant Colonel Francis Smith, not General Thomas Hall.
This disagrees with what you said.

(8) You said: {user_input_text}.
I checked: {suggested_question}
I found this article: {evidence_snippet}"""


fixing_with_evidence = """[web] I will fix some things you said.

(1) You said: Your nose switches back and forth between nostrils. When you sleep, you switch about every 45 minutes.
This is to prevent a buildup of mucus. It’s called the nasal cycle.
I checked: How often do your nostrils switch?
I found this article: Although we don’t usually notice it, during the nasal cycle one nostril becomes congested and thus
contributes less to airflow, while the other becomes decongested. On average, the congestion pattern switches about
every 2 hours, according to a small 2016 study published in the journal PLOS One.
This suggests 45 minutes switch time in your statement is wrong.
My fix: Your nose switches back and forth between nostrils. When you sleep, you switch about every 2 hours. This is to
prevent a buildup of mucus. It’s called the nasal cycle.

(2) You said: In the battles of Lexington and Concord, the British side was led by General Thomas Hall.
I checked: who led the British side in the battle of Lexington and Concord?
I found this article: Interesting Facts about the Battles of Lexington and Concord. The British were led by Lieutenant
Colonel Francis Smith. There were 700 British regulars.
This suggests General Thomas Hall in your statement is wrong.
My fix: In the battles of Lexington and Concord, the British side was led by Lieutenant Colonel Francis Smith.

(3) You said: The Stanford Prison Experiment was conducted in the basement of Encina Hall, Stanford’s psychology
building.
I checked: where was Stanford Prison Experiment conducted.
I found this article: Carried out August 15-21, 1971 in the basement of Jordan Hall, the Stanford Prison Experiment set
out to examine the psychological effects of authority and powerlessness in a prison environment.
This suggests Encina Hall in your statement is wrong.
My fix: The Stanford Prison Experiment was conducted in the basement of Jordan Hall, Stanford’s psychology building.

(4) You said: Phoenix Mills Ltd., a diversified business conglomerate, was established in 1854. It has a history of over
160 years.
I checked: When was Phoenix Mills Ltd. founded?
I found this article: Phoenix Mills Ltd was incorporated in the year 1905. The company began their operations as a
textile manufacturing company on 17.3 acres of land at Lower Parel in Mumbai. In the year 1959 the company was listed in
the Bombay Stock Exchange.
This suggests the year of establishment 1854 in your statement is wrong.
My fix: Phoenix Mills Ltd., a diversified business conglomerate, was established in 1854. It has a history of over 160
years.

(4) You said: The Havel-Hakimi algorithm is an algorithm for converting the adjacency matrix of a graph into its
adjacency list. It is named after Vaclav Havel and Samih Hakimi.
I checked: What is the Havel-Hakimi algorithm?
I found this article: The Havel-Hakimi algorithm constructs a special solution if a simple graph for the given degree
sequence exists, or proves that one cannot find a positive answer. This construction is based on a recursive algorithm.
The algorithm was published by Havel (1955), and later by Hakimi (1962).
This suggests the Havel-Hakimi algorithm’s functionality in your statement is wrong.
My fix: The Havel-Hakimi algorithm constructs a special solution if a simple graph for the given degree sequence exists,
or proves that one cannot find a positive answer. It is named after Vaclav Havel and Samih Hakimi

(5) You said: "Time of My Life" is a song by American singer-songwriter Bill Medley from the soundtrack of the 1987 film
Dirty Dancing. The song was produced by Phil Ramone.
I checked: Who was the producer of "(I’ve Had) The Time of My Life"?
I found this article: On September 8, 2010, the original demo of this song, along with a remix by producer Michael Lloyd
, was released as digital files in an effort to raise money for the Patrick Swayze Pancreas Cancer Resarch Foundation at
Stanford University.
This suggests "Time of My Life" producer name in your statement is wrong.
My fix: "Time of My Life" is a song by American singer-songwriter Bill Medley from the soundtrack of the 1987 film Dirty
Dancing. The song was produced by Michael Lloyd.

(6) You said: Phoenix Market City Pune is located on 21 acres of prime property in Pune. It is spread across four levels
with approximately 1.4 million square feet of built-up space. The mall is owned and operated by Phoenix Mills Limited.
I checked: What is the area of Phoenix Market City in Pune?
I found this article: Phoenix Market City was opened in January 2013 and has the distinction of being the largest mall
in the city of Pune, with the area of 3.4 million square feet. It is located in the Viman Nagar area of Pune.
This suggests the 1.4 million square feet of built-up space in your statment is wrong.
My fix: Phoenix Market City Pune is located on 21 acres of prime property in Pune. It is spread across four levels with
approximately 3.4 million square feet of built-up space. The mall is owned and operated by Phoenix Mills Limited.

(7) You said: {user_input_text}.
I checked: {suggested_question}
I found this article: {evidence_snippet}
This suggests"""


nasa_links = [
    "https://climate.nasa.gov/news/3231/climate-change-can-put-more-insects-at-risk-for-extinction/",
 "https://climate.nasa.gov/news/3230/satellites-help-scientists-track-dramatic-wetlands-loss-in-louisiana/",
 "https://climate.nasa.gov/news/3229/nasa-fieldwork-studies-signs-of-climate-change-in-arctic-boreal-regions/",
 "https://climate.nasa.gov/news/3228/methane-super-emitters-mapped-by-nasas-new-earth-space-mission/",
 "https://climate.nasa.gov/news/3226/nasa-to-discuss-latest-emit-findings-helps-address-climate-change/",
 "https://climate.nasa.gov/news/3223/nasa-dust-detective-delivers-first-maps-from-space-for-climate-science/",

 "https://climate.nasa.gov/news/3220/nasas-s-mode-field-campaign-deploys-to-the-pacific-ocean/",
 "https://climate.nasa.gov/news/3218/nasa-study-finds-climate-extremes-affect-landslides-in-surprising-ways/",
 "https://climate.nasa.gov/news/3215/testing-testing-space-bound-us-european-water-mission-passes-finals/",
 "https://climate.nasa.gov/news/3214/nasa-usgs-map-minerals-to-understand-earth-makeup-climate-change/",
 "https://climate.nasa.gov/news/3213/2022-arctic-summer-sea-ice-tied-for-10th-lowest-on-record/",
 "https://climate.nasa.gov/news/3206/nasa-studies-find-previously-unknown-loss-of-antarctic-ice/",
 "https://climate.nasa.gov/news/3205/nasa-data-on-plant-sweating-could-help-predict-wildfire-severity/",
 "https://climate.nasa.gov/news/3204/tonga-eruption-blasted-unprecedented-amount-of-water-into-stratosphere/",
"https://climate.nasa.gov/news/3203/nasas-mineral-dust-detector-starts-gathering-data/",
"https://climate.nasa.gov/news/3202/us-european-satellite-will-make-worlds-first-global-freshwater-survey/",
"https://climate.nasa.gov/news/3201/climate-patterns-thousands-of-miles-away-affect-us-bird-migration/",
"https://climate.nasa.gov/news/3198/nasas-new-mineral-dust-detector-readies-for-launch/",
"https://climate.nasa.gov/news/3197/nasa-highlights-climate-research-on-cargo-launch-sets-coverage/",
"https://climate.nasa.gov/news/3196/subpopulation-of-greenland-polar-bears-found-by-nasa-funded-study/",
"https://climate.nasa.gov/news/3193/nasas-ecostress-sees-las-vegas-streets-turn-up-the-heat/",
"https://climate.nasa.gov/news/3192/nasa-fema-release-comprehensive-climate-action-guide/",
"https://climate.nasa.gov/news/3184/a-force-of-nature-hurricanes-in-a-changing-climate/",
"https://climate.nasa.gov/news/3180/nasas-cynthia-rosenzweig-receives-2022-world-food-prize/",
"https://climate.nasa.gov/news/3176/nasas-ecostress-detects-heat-islands-in-extreme-indian-heat-wave/",
"https://climate.nasa.gov/news/3175/international-satellite-to-track-impacts-of-small-ocean-currents/",
"https://climate.nasa.gov/news/3171/nasas-emit-will-map-tiny-dust-particles-to-study-big-climate-impacts/",
"https://climate.nasa.gov/news/3157/california-field-campaign-is-helping-scientists-protect-diverse-ecosystems/",
"https://climate.nasa.gov/news/3156/connect-with-nasa-on-social-media-this-earth-day/",
"https://climate.nasa.gov/news/3154/international-sea-level-satellite-takes-over-from-predecessor/",
"https://climate.nasa.gov/news/3150/nasa-finds-each-state-has-its-own-climatic-threshold-for-flu-outbreaks/",
"https://climate.nasa.gov/news/3149/california-fire-led-to-spike-in-bacteria-cloudiness-in-coastal-waters/",
"https://climate.nasa.gov/news/3146/sea-level-to-rise-up-to-a-foot-by-2050-interagency-report-finds/",
"https://climate.nasa.gov/news/3140/2021-tied-for-6th-warmest-year-in-continued-trend-nasa-analysis-shows/",
"https://climate.nasa.gov/news/3139/six-questions-to-help-you-understand-the-6th-warmest-year-on-record/",
"https://climate.nasa.gov/news/3134/reducing-emissions-to-lessen-climate-change-would-yield-dramatic-health-benefits-by-2030/"
]


nexus_links = ['https://regeneration.org/nexus/afforestation',
 'https://regeneration.org/nexus/agroecology',
 'https://regeneration.org/nexus/agroforestry',
 'https://regeneration.org/nexus/asparagopsis',
 'https://regeneration.org/nexus/azolla-fern',
 'https://regeneration.org/nexus/bamboo',
 'https://regeneration.org/nexus/beavers',
 'https://regeneration.org/nexus/biochar',
 'https://regeneration.org/nexus/buildings',
 'https://regeneration.org/nexus/clean-cookstoves',
 'https://regeneration.org/nexus/compost',
 'https://regeneration.org/nexus/degraded-land-restoration',
 'https://regeneration.org/nexus/eating-plants',
 'https://regeneration.org/nexus/education-girls',
 'https://regeneration.org/nexus/electric-vehicles',
 'https://regeneration.org/nexus/electrify-everything',
 'https://regeneration.org/nexus/energy-storage',
 'https://regeneration.org/nexus/fifteen-minute-city',
 'https://regeneration.org/nexus/fire-ecology',
 'https://regeneration.org/nexus/grasslands',
 'https://regeneration.org/nexus/heat-pumps',
 'https://regeneration.org/nexus/mangroves',
 'https://regeneration.org/nexus/marine-protected-areas',
 'https://regeneration.org/nexus/micromobility',
 'https://regeneration.org/nexus/nature-of-cities',
 'https://regeneration.org/nexus/net-zero-cities',
 'https://regeneration.org/nexus/offsets',
 'https://regeneration.org/nexus/ocean-farming',
 'https://regeneration.org/nexus/regenerative-agriculture',
 'https://regeneration.org/nexus/seaforestation',
 'https://regeneration.org/nexus/seagrasses',
 'https://regeneration.org/nexus/silvopasture',
 'https://regeneration.org/nexus/smart-microgrids',
 'https://regeneration.org/nexus/solar',
 'https://regeneration.org/nexus/tidal-salt-marshes',
 'https://regeneration.org/nexus/tropical-forests',
 'https://regeneration.org/nexus/urban-farming',
 'https://regeneration.org/nexus/urban-mobility',
 'https://regeneration.org/nexus/wetlands',
 'https://regeneration.org/nexus/wind']
