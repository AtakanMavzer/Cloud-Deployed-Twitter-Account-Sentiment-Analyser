const fs = require('fs');
const puppeteer = require('puppeteer');
const ar = [];

const { MongoClient } = require("mongodb");
const args1= process.argv[2];

const twitUrl=`https://twitter.com/${args1}`;
const pass=process.env.password;
var url=`mongodb+srv://NodeJs:${pass}@sentiment.6g24c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority`

// Replace the uri string with your MongoDB deployment's connection string.

const client = new MongoClient(url);
async function sendData(dataTweet) {
  try {
    await client.connect();
    const database = client.db("myFirstDatabase");
    const sentiment = database.collection("sentiment");
    // create a document to be inserted
    const doc = { acc: args1, tweets: dataTweet };
    const result = await sentiment.insertOne(doc);
    console.log(
      `${result.insertedCount} documents were inserted with the _id: ${result.insertedId}`,
    );
  } finally {
    await client.close();
  }
}



let index = 0;

(async () => {
    const browser = await puppeteer.launch({
        executablePath: '/usr/bin/chromium-browser',
        'args': ['--no-sandbox',
        "--disabled-setupid-sandbox"],
        headless: true
    });
    const page = await browser.newPage();
    await page.goto(twitUrl);
    await page.setViewport({
        width: 1200,
        height: 800
    });
    await page.waitFor(2000);
    let resText = []

    let res = [], time = [], timeText = [], idx = [], retweet = [], likes = [], comments = [];
    for (let i = 0; i < 3; i++) {
        let js = await autoScroll(page).then(console.log(i));
        for (let z = 0; z < js[0].length; z++) {
            res.push(js[0][z]);
     //       time.push(js[1][z]);
            timeText.push(js[1][z]);
            retweet.push(js[2][z]);
            likes.push(js[3][z]);
            comments.push(js[4][z]);
        }

    }

    res = res.filter((x, i, a) => {
        if (a.indexOf(x) === i) { idx.push(i); }
        return res[i];
    });
    //console.log("filter ", res);
    finalJ = [];
    for (let a = 0; a < idx.length; a++) {
        finalJ.push( 
            {
            "tweet": res[idx[a]],
            "date": timeText[idx[a]],
            "retweet": retweet[idx[a]],
            "likes": likes[idx[a]],
            "comments": comments[idx[a]]
        }
    )}
    finalJ = JSON.stringify(finalJ);
    process.stdout.write(finalJ);
    /*
    fs.writeFile('Data.txt', finalJ, function (err) {
        if (err) return console.log(err);
        console.log('Hello World > helloworld.txt');
    });*/

    console.log(finalJ);
    await browser.close();
    
    sendData(res);
    
})();

async function autoScroll(page) {
    let results = await page.$$eval('article div[lang]', (tweets) => tweets.map((tweet) => tweet.textContent));
    let timeText = await page.$$eval('article  time[datetime]', (tweets) => tweets.map((tweet) => tweet.textContent));
    let retweet = await page.$$eval('article div[data-testid="retweet"]', (tweets) => tweets.map((tweet) => tweet.textContent));
    let likes = await page.$$eval('article div[data-testid="like"]', (tweets) => tweets.map((tweet) => tweet.textContent));
    let comments = await page.$$eval('article div[data-testid="reply"]', (tweets) => tweets.map((tweet) => tweet.textContent));

    await page.evaluate(async () => {
        await new Promise((resolve, reject, page) => {
            var totalHeight = 0;
            var distance = 200;
            var timer = setInterval((page) => {

                var scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;
                
                console.log("th ", totalHeight);
                if (totalHeight % 5000 == 0) {
                    window.scrollBy(0, -2500);
                }
                if ((totalHeight > 3000)) {
                    //|| totalHeight >= scrollHeight) {
                    clearInterval(timer);
                    resolve(page);
                }
            }, 200);
        })
    });
    resJ = {}

    
    for (i = 0; i < results.length; i++) {
        a = {
            "tweet": results[i],
            "date": timeText[i],
            "retweet": retweet[i],
            "likes": likes[i],
            "comments": comments[i]

        }
        resJ[`tweet_${index}`] = a
        index++;

    }
    //console.log(resJ);
    ar.push(results);

    return [results, timeText, retweet, likes, comments];

    //return resJ;

}