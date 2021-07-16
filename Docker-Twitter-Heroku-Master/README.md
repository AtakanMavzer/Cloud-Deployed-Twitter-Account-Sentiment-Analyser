# docker-twitter
Decisions:

We decided to use Docker for our container since our project needs
cloud deployment.

For the Database, we decided to use MongoDB for its NoSQL attribute and
ease to use in compatibility with our project. Simple data holding was enough
for us.

Twitter gathering is done by Scraping with Node.js Puppeteer. We built a scraper
because the Twitter did not give us permission to use their API. Scraper was the
most difficult part in our project, since reading through DOM was not very user friendly
at first.

For API and Sentiment analysis, we decided to use Python, FLASK and TextBlob. Using these
libraries increased our speed in deployment but using Docker with Flask required us to learn
new things. "wsgi.py"
