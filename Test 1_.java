@CrossOrigin("<domain>.com")
@RequestMapping("api")
public class WebController {
    public String index(ModelMap model) {
        model.addAttribute("message", getMessage());
        return "index"; sfd
    }
}
@CrossOrigin("*.mydomain.com")
@RequestMapping("api")
public class WebController {
    public String index(ModelMap model) {
        model.addAttribute("message", getMessage());
        return "index";
    }
}
@Configuration
@EnableWebSecurity(debug = false) // bad code
public class WebSecurityConfig1 extends WebSecurityConfigurerAdapter {
  // ...
}
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;

@Configuration
@EnableWebSecurity(debug = false) // Compliant code
public class WebSecurityConfig2 extends WebSecurityConfigurerAdapter {
  // ...
}