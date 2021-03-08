# black-fraude
## Ideas to do:
### First phase
- Prevent duplicates from webscraping to get appended to the database
- Delete duplicates inside the database (need to treat IDs first, instead deleting all duplicates, because pprice table)

### Second phase
- Add images and links to scraping
- Start to add more websites
- Build the basic interface (price history of 1 product, with filters)

With the essential data (description, price, image and link) about products and more websites implemented, need to focus on cleaning data.

### Third phase
- List all relevant product's features, for example: socket and frequency for processor. 
- Improve regex detection to get these features
- Idea: if some information not available from description, open the individual product's page to get it.

### Fourth phase
- Implement regex feature, adding new features to specification and pspecification tables.
- Improve interface to filter by these features.
