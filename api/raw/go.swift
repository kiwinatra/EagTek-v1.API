import HTTPConnection
import HTTPS
import APICore
import EagTek
import ./req

public class Eag_HomePath readonly {
    var Base = "https://eaglercraft.com/__/"
    var allowed_apis = "
    https://api.eagl.to
    https://kiwinatra.github.io/api
    https://api.eagteka.at/__/
    "
}


case 200 ... 209 {
    req.show("MQL Error :(")
    innerHTML.show(
        .req"
            <div class="error 209 case mvp" >
            {error}
            </div>
        "
    )

}