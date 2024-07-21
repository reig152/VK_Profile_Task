using System;
using System.Net.Http;
using System.Threading.Tasks;
// Пакет для парсинга html кода
using HtmlAgilityPack;

class SteamParser
{
    static async Task Main()
    {
        // Ссылка на страницу с топом продаж в Steam
        var url = "https://store.steampowered.com/search/?filter=topsellers";

        // Создание HTTP-клиента
        var httpClient = new HttpClient();

        try
        {
            // Отправка GET-запроса к указанной ссылке
            var response = await httpClient.GetAsync(url);

            // Проверка успешности ответа
            if (response.IsSuccessStatusCode)
            {
                // Чтение содержимого ответа как строки
                var html = await response.Content.ReadAsStringAsync();

                // Создание документа HTML
                var doc = new HtmlDocument();
                doc.LoadHtml(html);

                // Поиск узлов с играми
                var gameNodes = doc.DocumentNode.SelectNodes("//div[@id='search_resultsRows']/a");

                // Проверка, найдены ли узлы с играми
                if (gameNodes != null)
                {
                    int count = 0;
                    foreach (var gameNode in gameNodes)
                    {
                        // Получение первых 10 игр
                        if (count >= 10)
                            break;

                        // Извлечение названия игры
                        var titleNode = gameNode.SelectSingleNode(".//span[@class='title']");
                        var title = titleNode?.InnerText.Trim();

                        // Извлечение цены игры
                        var priceNode = gameNode.SelectSingleNode(
                            ".//div[contains(@class, 'col search_price_discount_combined responsive_secondrow')]"
                        );
                        var price = priceNode?.SelectSingleNode(
                            ".//div[contains(@class, 'discount_final_price')]"
                        )?.InnerText.Trim();

                        // Вывод информации топа игр в консоль
                        Console.WriteLine($"{count + 1} {title} {price}");

                        count++;
                    }
                }
                else
                {
                    // Обработка случая, если узлы с играми не найдены
                    Console.WriteLine("Не удалось найти игры на странице.");
                }
            }
            else
            {
                // Обработка ошибочного ответа запроса
                Console.WriteLine(
                    $"Не удалось загрузить страницу. Код состояния: {response.StatusCode}"
                );
            }
        }
        catch (Exception e)
        {
            // Обработка других исключений
            Console.WriteLine($"Ошибка обработки HTML: {e.Message}");
        }
    }
}
