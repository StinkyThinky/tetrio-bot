This repo documents my naive experiments and a learning journey:

Summer of 2025, I decided it would be cool to build a tetris bot!

I had no idea where to start (complete beginner), so I began looking through different videos and examples. 

Eventually, I realised the task I gave myself was a bit too advanced at the time, so I would instead take some "inspiration" and improve upon an existing bot.
I soon came upon Yilinho's bot, and I chose it as it was the only python bot I could find at the time that played tetris to an acceptable level. 
I spent a few days reading through the code, and found areas for improvement.

Changes:
I was working on Mac, and many libraries used weren't supported or were just outdated, so I created my own code for video processing, though still using the existing structure. 
Implemented J/L spins, as well as adding more cases for Z/S spins. 
My tetrio was also quite laggy so I switched to Jstris and downloaded Ultra so it can be played offline and have no lag. 

I also decided that the internal parameter weights were set arbitrarily and could be refined to be better.
I watched 1 machine learning video and naively decided that I could develop my own approach to machine learning in order to refine these parameters. In hindsight, I basically created my own bootleg reinforcement learning approach. During training I often noticed the bot took a liking to high board height and taking greedy Tspins. I ended up with a bot that I think indeed "improved", though my metrics for performance and improvement were dubious so take this entire project with a grain of salt...

Today, I know there are many improvements to my method to be made and I plan to build my own bot from scratch!
