using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.Web.UI;

public partial class EaglerCraftAPI : Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
    }

    protected async void btnGetData_Click(object sender, EventArgs e)
    {
        string apiUrl = "https://api.eaglercraft.com/v1"; 
        string result = await GetApiData(apiUrl);
        lblResult.Text = result;
    }

    private async Task<string> GetApiData(string url)
    {
        using (HttpClient client = new HttpClient())
        {
            try
            {
                HttpResponseMessage response = await client.GetAsync(url);
                response.EnsureSuccessStatusCode();
                return await response.Content.ReadAsStringAsync();
            }
            catch (Exception ex)
            {
                return "Error: " + ex.Message;
            }
        }
    }
}
