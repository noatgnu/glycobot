import time

from base_parser import BaseParser, Author, Article

base_url = "https://chemrxiv.org/api/items?types=&itemTypes=&licenses=&orderBy=relevant&orderType=desc&limit=40&offset=0&search=glycosylation&institutionId=259"


class ChemRxivParser(BaseParser):
    def __init__(self, base_url="https://chemrxiv.org/engage/api-gateway/chemrxiv/graphql", limit=100):
        super().__init__(base_url)
        self.current_offset = 0
        self.limit = limit
        self.current_page = 0

    def search(self, terms, max_page=10, break_entry=None):
        data = {
            "query": "query searchDashboardPageLoad(\n  $text: String = \"\",\n  $subjects: [String!],"
                     "\n  $categories: [String!],\n  $events: [String!],\n  $publishedDates: [String!],\n  $partners: "
                     "[String!],\n  $contents: [String!],\n  $keywords: [String!],\n  $authors: String = \"\","
                     "\n  $skip: Int = 0,\n  $limit: Int = 10,\n  $sortBy: SortByEnum = PUBLISHED_DATE_DESC\n  ) {\n  "
                     "viewer {\n    usageEventsDisabled\n\n    user {\n      ...userRoleFragment\n    }\n\n    "
                     "searchItems(\n      searchTerm: $text,\n      subjectKeys: $subjects,\n      categoryKeys: "
                     "$categories,\n      eventKeys: $events,\n      publishedDateKeys: $publishedDates,"
                     "\n      partnerKeys: $partners,\n      contentTypeKeys: $contents,\n      keywordsKeys: "
                     "$keywords,\n      searchAuthor: $authors,\n      skip: $skip,\n      limit: $limit,"
                     "\n      sortBy: $sortBy\n      ) {\n      totalCount\n\n      results: itemHits {\n        "
                     "highlight {\n          text\n          matchPositions {\n            start\n            end\n   "
                     "       }\n        }\n\n        item {\n          ...itemMatchFragment\n        }\n      }\n\n   "
                     "   subjectBuckets {\n        ...searchBucketFragment\n      }\n\n      categoryBuckets {\n      "
                     "  ...searchBucketFragment\n      }\n\n      eventBuckets {\n        ...searchBucketFragment\n   "
                     "   }\n\n      partnerBuckets {\n        ...searchBucketFragment\n      }\n\n      "
                     "publishedDateBuckets {\n        ...searchBucketFragment\n      }\n\n      contentBuckets: "
                     "contentTypeBuckets {\n        ...searchBucketFragment\n      }\n\n      dateBuckets: "
                     "publishedDateBuckets {\n        ...searchBucketFragment\n      }\n    }\n\n    subjectTypes: "
                     "subjects {\n      ...subjectTypeFragment\n    }\n\n    contentTypes {\n      "
                     "...contentTypeFragment\n    }\n\n    categoryTypes: categories {\n      "
                     "...categoryTypeFragment\n    }\n  }\n}\n\nfragment userRoleFragment on User {\n  __typename\n  "
                     "id\n  sessionExpiresAt\n  titleTypeId: title\n  firstName\n  lastName\n  emailAddress : email\n "
                     " orcid\n  roles\n  accountType\n}\n\nfragment itemMatchFragment on MainItem {\n  __typename\n  "
                     "id\n  title\n  abstract\n  keywords\n  origin\n  subjectType: subject {\n    "
                     "...subjectTypeFragment\n  }\n  contentType {\n    ...contentTypeFragment\n  }\n  categoryTypes: "
                     "categories {\n    ...categoryTypeFragment\n  }\n  mainCategory {\n    name\n  }\n  asset{\n    "
                     "mimeType\n    original{\n      url\n    }\n  }\n  authors {\n    title\n    firstName\n    "
                     "lastName\n    authorConfirmationId\n    displayOrder\n  }\n  metrics {\n    metricType\n    "
                     "description\n    value\n    unit\n  }\n}\n\nfragment searchBucketFragment on SearchBucket {\n  "
                     "__typename\n  count\n  key\n  label\n}\n\nfragment subjectTypeFragment on Subject {\n  "
                     "__typename\n  id\n  name\n  description\n}\n\nfragment contentTypeFragment on ContentType {\n  "
                     "__typename\n  id\n  name \n  allowJournalSubmission\n}\n\nfragment categoryTypeFragment on "
                     "Category {\n  __typename\n  id\n  name\n  description\n  parentId\n}\n",
            "variables": {
                "text": terms,
                "skip": 0,
                "categories": [], "contents": [], "events": [], "publishedDates": ["LAST_MONTH"], "subjects": [], "partners": [],
                "keywords": []
            }
        }
        response = self._request(self.base_url, data=data, request_type='POST')
        entries = []
        content = response.json()
        count = content["data"]["viewer"]["searchItems"]["totalCount"]
        stop = False
        for i in content["data"]["viewer"]["searchItems"]["results"]:

            if break_entry:
                if break_entry == str(i["item"]["id"]):
                    stop = True
                    break
            authors = []

            for a in i["item"]["authors"]:
                authors.append(Author(a["firstName"], a["lastName"]))
            entries.append(
                Article(i["item"]["title"], "https://chemrxiv.org/engage/chemrxiv/article-details/" + i["item"]["id"],
                        authors,
                        id=str(i["item"]["id"]), source="ChemRxiv"))
        if not stop:
            for n in range(len(entries), count, len(entries)):
                time.sleep(1)
                if stop:
                    break
                data["variables"]["skip"] = n
                response = self._request(self.base_url, data=data, request_type='POST')
                content = response.json()

                for i in content["data"]["viewer"]["searchItems"]["results"]:
                    if break_entry:
                        if break_entry == str(i["item"]["id"]):
                            stop = True
                            break
                    authors = []

                    for a in i["item"]["authors"]:
                        authors.append(Author(a["firstName"], a["lastName"]))
                    entries.append(
                        Article(i["item"]["title"], "https://chemrxiv.org/engage/chemrxiv/article-details/" + i["item"]["id"],
                                authors,
                                id=str(i["item"]["id"]), source="ChemRxiv"))

        yield entries

        # if len(content["items"]) == self.limit and self.current_page < max_page:
        #     print(self.limit, self.current_page, max_page)
        #     self.current_offset += self.limit
        #     yield from self.search(terms, max_page)
        #     self.current_page += 1


def get_chemrxiv(args):
    stop_art = None
    p = ChemRxivParser(base_url=args.cu)
    a = []
    for n, i in enumerate(p.search(
            'glycosylation or lectin or carbohydrate or glycoprotein or glycan or glycosyltransferase or sialic',
            max_page=args.max, break_entry=args.sc)):
        if len(i) > 0:
            if n == 0:
                stop_art = i[0].id
            a += i
    p.close()
    return a, stop_art
