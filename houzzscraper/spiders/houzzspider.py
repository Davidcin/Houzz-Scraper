import scrapy
import json
import requests

class HouzzSpider(scrapy.Spider):
    name = "houzzspider"
    allowed_domains = ["houzz.com"]
    start_urls = ["https://www.houzz.com/professionals/general-contractor/los-angeles-ca-us-probr0-bo~t_11786~r_5368361"]

    count = 0
    count1 = 0
    project_count = 0

    def parse(self, response):
        # contractors = response.css('a.hz-pro-ctl::attr(href)').extract()
        # url = response.css('a.hz-pro-ctl::attr(href)').get()  # single url
        
        #? https://www.houzz.com/professionals/general-contractors/88-builders-group-pfvwus-pf~789557516  88group
        #? https://www.houzz.com/professionals/general-contractors/rodo-development-inc-pfvwus-pf~918996204 rodo
        # https://www.houzz.com/professionals/general-contractors/american-home-improvement-inc-pfvwus-pf~2014924747
        url = "https://www.houzz.com/professionals/general-contractors/rodo-development-inc-pfvwus-pf~918996204" # single url
        # contractors = ["https://www.houzz.com/professionals/general-contractors/88-builders-group-pfvwus-pf~789557516", "https://www.houzz.com/professionals/general-contractors/rodo-development-inc-pfvwus-pf~918996204"] # single url


        # for url in contractors:
        #     HouzzSpider.count+=1
        #     print("####################")
        #     print(HouzzSpider.count, url)
        yield response.follow(url, callback=self.parse_contractor_page)

        # next_page = response.css("a.hz-pagination-link--next::attr(href)").get()
        # relative_url = "houzz.com" + next_page
        # print("000000000000000000000000", relative_url)
        # if next_page is not None and next_page[-2:] != "30":
        #     yield response.follow(relative_url, callback=self.parse)
            
# json.loads(response.css('script#hz-ctx::text').get())

    def parse_contractor_page(self, response):
        data = json.loads(response.css('script#hz-ctx::text').get())

        #! file = open(f"1data/{HouzzSpider.count1}.json", "w")
        #! file.write(json.dumps(data, indent=2))

        # displayName = data["data"]["stores"]["data"]["ProProfileStore"]["data"]["user"]["displayName"]

        id = data["data"]["stores"]["data"]["ProProfileStore"]["data"]["user"]["id"]
        project_count = data["data"]["stores"]["data"]["ProProfileStore"]["data"]["user"]["stats"]["projectsCount"]
        projects_url = f'https://www.houzz.com/j/ajax/profileProjectsAjax?userId={id}&fromItem=0&itemsPerPage={project_count}'

        headers = {'x-requested-with': 'XMLHttpRequest',}
        projects_data = requests.request("GET", projects_url, headers=headers)

        
        project_ids = projects_data.json()["ctx"]["data"]["stores"]["data"]["ProProfileStore"]["data"]["projects"]

        #! file = open(f"21dat.json", "w")
        #! file.write(json.dumps(projects_data.json()))

        for project_id in project_ids:
            id = str(project_id)
            project_url = f"https://www.houzz.com/hznb/projects/-pj-vj~{id}"
            projects = yield response.follow(project_url, callback=self.parse_project)
        yield {
            "displayName": data["data"]["stores"]["data"]["ProProfileStore"]["data"]["user"]["displayName"],
            "href":    data["data"]["stores"]["data"]["MetaDataStore"]["data"]["htmlMetaTags"][1]["attributes"]["href"],
            "isProfessional": data["data"]["stores"]["data"]["ProProfileStore"]["data"]["user"]["isProfessional"],
            "brandProfile": data["data"]["stores"]["data"]["ProProfileStore"]["data"]["user"]["brandProfile"],
            "id": data["data"]["stores"]["data"]["ProProfileStore"]["data"]["user"]["professional"]["id"],
            "titleSlug": data["data"]["stores"]["data"]["ProProfileStore"]["data"]["user"]["professional"]["seoHint"]["paths"]["ViewProfessional"]["titleSlug"],
            "numReviews": data["data"]["stores"]["data"]["ProProfileStore"]["data"]["user"]["professional"]["numReviews"],
            "location": data["data"]["stores"]["data"]["ProProfileStore"]["data"]["user"]["professional"]["location"],
            "projects": [projects],
        }




# ["data"]["stores"]["data"]["ProjectStore"]["data"]["7078290"]["costRangeString"] am adgilasaa json path mayutis
# json requests aketebs es yleoba projectebi yvela ar moaqvs ert zaxodze
# karoche payloadshi shedi naxe ra queriebs ugzavni da gauzarde per page query naxe tu wamoigebs
#  tu ar wamoigo shemayare ukanwE

# userId = data["data"]["stores"]["data"]["ProProfileStore"]["data"]["user"]["id"]
# total_projects = len(data["data"]["stores"]["data"]["ProProfileStore"]["data"]["projects"])

# project_url = f"https://www.houzz.com/j/ajax/profileProjectsAjax?userId={userId}&fromItem=0&itemsPerPage={total_projects}&shareLevel=PUBLIC_ONLY"



    def parse_project(self, response):
        project_data = json.loads(response.css('script#hz-ctx::text').get())
        # title = project_data["data"]["stores"]["data"]["MetaDataStore"]["data"]["htmlMetaTags"][1]["attributes"]["content"]
        
        #! file = open(f"1projects/{title}.json", "w")
        #! file.write(json.dumps(project_data, indent=2))
        
        project_id = str(project_data["data"]["stores"]["data"]["ViewProjectPageStore"]["data"]["current_project_id"])
        
        try:
            year = project_data["data"]["stores"]["data"]["ProjectStore"]["data"][project_id]["yearStarted"]
            cost = project_data["data"]["stores"]["data"]["ProjectStore"]["data"][project_id]["costRangeString"]
        except KeyError:
            year = "year not specified"
            cost = "cost not specified"

        yield {
            "title": project_data["data"]["stores"]["data"]["MetaDataStore"]["data"]["htmlMetaTags"][1]["attributes"]["content"],
            "projectId": project_id,
            "year": year,
            "cost": cost
        }












    #     books = response.css('article.product_pod')
    #     for book in books:
    #         relative_url = book.css('h3 a::attr(href)').get()
    #         if "catalogue/" not in relative_url:
    #             book_url = "https://books.toscrape.com/catalogue/" + relative_url
    #         else:
    #             book_url = "https://books.toscrape.com/" + relative_url
    #         yield response.follow(book_url, callback = self.parse_book_page)

    #         next_page = response.css('li.next a::attr(href)').get()
    #         if next_page is not None and next_page != "page-3.html":
    #             if "catalogue/" not in next_page:
    #                 next_page_url = "https://books.toscrape.com/catalogue/" + next_page
    #             else:
    #                 next_page_url = "https://books.toscrape.com/" + next_page
    #             yield response.follow(next_page_url, callback = self.parse)


    # def parse_book_page(self, response):
    #     yield {
    #         "url": response.url,
    #         "title": response.css('article.product_page div.product_main h1::text').get(),
    #         "price": response.css('article.product_page div.product_main p.price_color::text').get()
    #     }