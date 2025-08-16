<%@ Page Language="C#" AutoEventWireup="true" CodeFile="EaglerCraftAPI.aspx.cs" Inherits="EaglerCraftAPI" %>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>EaglerCraft API Example</title>
</head>
<body>
    <form id="form1" runat="server">
        <div>
            <h2>EaglerCraft API Request</h2>
            <asp:Button ID="btnGetData" runat="server" Text="Get Data" OnClick="btnGetData_Click" />
            <br /><br />
            <asp:Label ID="lblResult" runat="server" Text=""></asp:Label>
        </div>
    </form>
</body>
</html>
