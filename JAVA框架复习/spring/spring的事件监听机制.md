#### Spring的事件监听机制

* Spring 事件监听机制的本质是观察者模式的应用，包括事件、事件监听器、事件发布器等主要组件。
* **事件（Event）**：一个实现了 ApplicationEvent 类的对象，代表了应用程序中的某个特定事件。我们可以根据需要创建自定义事件，只要继承 ApplicationEvent 类并添加相关的属性和方法就可以了。
* **事件监听器（Event Listener）：实现了 ApplicationListener<E> 接口的对象，其中 E 表示监听器需要处理的事件类型。监听器可以通过 onApplicationEvent(E event) 方法处理接收到的事件。另外，也可以使用 @EventListener 注解简化事件监听器的实现，技术派采用的正是这种方式。**
* **事件发布器（Event Publisher）：事件发布器负责将事件发布给所有关注该事件的监听器。在 Spring 中，ApplicationEventPublisher 接口定义了事件发布的基本功能，而 ApplicationEventPublisherAware 接口允许组件获取到事件发布器的引用。Spring 的核心容器 ApplicationContext 实现了 ApplicationEventPublisher 接口，因此在 Spring 应用中，通常直接使用 ApplicationContext 作为事件发布器，技术派采用的正是这种方式。**



* 创建自定义事件

  



```java
@RestController
@RequestMapping(path = {"/api/admin/login", "/admin/login"})
public class AdminLoginController {

    @Autowired
    private UserService userService;

    @Autowired
    private SessionService sessionService;

    @PostMapping(path = {"", "/"})
    public ResVo<BaseUserInfoDTO> login(HttpServletRequest request,
                                        HttpServletResponse response) {
        //获取用户名
        String user = request.getParameter("username");
        //密码
        String pwd = request.getParameter("password");
        BaseUserInfoDTO info = userService.passwordLogin(user, pwd);
        String session = sessionService.login(info.getUserId());
        if (StringUtils.isNotBlank(session)) {
            // cookie中写入用户登录信息
            response.addCookie(new Cookie(SessionService.SESSION_KEY, session));
            return ResVo.ok(info);
        } else {
            return ResVo.fail(StatusEnum.LOGIN_FAILED_MIXED, "登录失败，请重试");
        }
    }

    @Permission(role = UserRole.LOGIN)
    @RequestMapping("logout")
    public ResVo<Boolean> logOut(HttpServletResponse response) throws IOException {
        Optional.ofNullable(ReqInfoContext.getReqInfo()).ifPresent(s -> sessionService.logout(s.getSession()));
        // 重定向到首页
        response.sendRedirect("/");
        return ResVo.ok(true);
    }
}
```

