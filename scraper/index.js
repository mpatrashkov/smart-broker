const axios = require("axios")
const fs = require("fs")
const cheerio = require("cheerio")

const HttpsProxyAgent = require("https-proxy-agent")
const SocksAgent = require("axios-socks5-agent")
const { getPhotoUrls, getPhoneFromElement } = require("./utils")

const regex_tel = /tel:(\d+)/g
const regex_photos = /user_files\/m\/.*\/(\d+_\d*_big\.jpg)/g

const example_url = "https://www.alo.bg/8157555"
const base_url = "https://www.alo.bg/"
const proxy_check_url = "https://httpbin.org/get?working=true"

const listings = []

async function main() {
    const listing_data = {
        id: 0,
        url: "",
        from: "",
        name: "",
        description: "",
        price: 0,
        price_string: "",
        currency: "",
        pricesqm: 0,
        year: 0,
        type: "",
        address: "",
        area: "",
        buildingType: "",
        floor: "",
        floorNumber: "",
        status: "",
        agents: [],
        // extras: { // TODO
        //     elevator: false,
        //     parking: false,
        //     furnished: false,
        // },
        extras: [],
        photos: [],
    }

    const data = await axios(example_url)
    const $ = cheerio.load(data.data)
    const id = parseInt(
        example_url.split("/")[example_url.split("/").length - 1]
    )
    const name = $(".large-headline.highlightable").text().trim()
    const description = $(".word-break-all.highlightable").text().trim()
    listing_data.id = id
    listing_data.url = example_url
    listing_data.name = name
    listing_data.description = description
    await Promise.all(
        $(".agent_div").map(async (i, element) => {
            const agentName = $(element).find(".contact_value").text().trim()
            const agentRole = $(element).find(".contact_info").text().trim()

            const result = await Promise.all(
                $(element)
                    .find(".contact_phone")
                    .map(async (i, element) => {
                        return await getPhoneFromElement(element)
                    })
            )

            listing_data.agents.push({
                agent_name: agentName,
                agent_role: agentRole,
                phones: result,
            })
        })
    )
    $(".ads-params-multi").map((i, element) => {
        const text = $(element).text().trim()
        listing_data.extras.push(text)
    })
    $(".ads-params-row").map((i, element) => {
        const text = $(element).text().trim()
        console.log(text)
        const rowData = text.split(":")[1].trim()
        const splittedText = text.split(":")
        if (text.includes("Година на строителство")) {
            if (text.match(/\d{4}/)) {
                listing_data.year = parseInt(rowData.match(/\d{4}/)[0])
            } else {
                listing_data.year = "Unknown"
            }
        } else if (text.includes("Квадратура")) {
            listing_data.area = rowData
        } else if (text.includes("Вид строителство")) {
            listing_data.buildingType = rowData
        } else if (text.includes("Вид на имота")) {
            listing_data.type = rowData
        } else if (text.includes("Степен на завършеност")) {
            listing_data.status = rowData.split(" ")[0]
        } else if (text.includes("Местоположение")) {
            listing_data.address = rowData
                .replace(/ +(?= )/g, "")
                .split(", (")[0]
        } else if (text.includes("Номер на етажа")) {
            listing_data.floorNumber = parseInt(rowData.match(/\d+/)[0])
        } else if (text.includes("Етаж")) {
            listing_data.floor = rowData
        } else if (text.includes("Цена")) {
            const pricePerSQM = $(element)
                .find(".ads-params-price-sub")
                .text()
                .trim()
            const priceWithCurrency = rowData.replace(pricePerSQM, "")
            const priceWithCurrencyNoSpaces = priceWithCurrency.replace(
                /\s/g,
                ""
            )
            const currency = priceWithCurrencyNoSpaces.match(/[a-zA-Z]{3}/g)[0]
            const price = parseFloat(
                priceWithCurrencyNoSpaces.replace(currency, "")
            )
            listing_data.currency = currency
            listing_data.price = price
            listing_data.price_string = priceWithCurrency
        } else if (text.includes("Обява от")) {
            splittedText.shift()
            listing_data.from = splittedText.join(":").trim()
        }
    })
    listing_data.pricesqm = parseInt(
        listing_data.price / parseInt(listing_data.area.split(" ")[0])
    )
    const photoUrls = getPhotoUrls($("#images-wrapper").html())
    listing_data.photos = photoUrls
    console.log(listing_data)
}

main()
