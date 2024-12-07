#### jwt

* 传统的方式
  * http协议本身是一种无状态的协议，如果用户向服务器提供了用户名和密码来进行用户认证，下次请求时，用户还要再一次进行用户认证才行。因为根据http协议，服务器并不能知道是哪个用户发出的请求，所以为了让我们的应用能识别是哪个用户发出的请求，我们只能在服务器存储─份用户登录的信息，这份登录信息会在响应时传递给浏览器，告诉其保存为cookie,以便下次请求时发送给我们的应用，这样应用就能识别请求来自哪个用户。
  * 暴露的问题
    * 用户经过应用认证后，应用都要在服务端做一次记录，以方便用户下次请求的鉴别，通常而言session都是保存在内存中，而随着认证用户的增多，服务端的开销会明显增大；
    * ==用户认证后，服务端做认证记录，如果认证的记录被保存在内存中的话，用户下次请求还必须要请求在这台服务器上，这样才能拿到授权的资源。在分布式的应用上，限制了负载均衡器的能力。==以此限制了应用的扩展能力；
    * ==session是基于cookie来进行用户识别，cookie如果被截获，用户很容易受到CSRF（跨站伪造请求攻击)攻击；==
    * 在前后端分离系统中应用解耦后增加了部署的复杂性。通常用户一次请求就要转发多次。如果用session每次携带sessionid到服务器，服务器还要查询用户信息。同时如果用户很多。这些信息存储在服务器内存中，给服务器增加负担。还有就是sessionid就是一个特征值，表达的信息不够丰富。不容易扩展。而且如果你后端应用是多节点部署。那么就需要实现session共享机制。不方便集群应用。
* jwt
  * 前端通过Web表单将自己的用户名和密码发送到后端的接口。该过程一般是HTTP的POST请求。建议的方式是通过SSL加密的传输(https协议)，从而避免敏感信息被嗅探。
  
  * 后端核对用户名和密码成功后，将用户的id等其他信息作为JWT Payload(负载)，将其与头部分别进行Base64编码拼接后签名，形成一个JWT(Token)。
  
  * 后端将JWT字符串作为登录成功的返回结果返回给前端。前端可以将返回的结果保存在localStorage（浏览器本地缓存）或sessionStorage（session缓存）上，退出登录时前端删除保存的JWT即可。
  
  * 前端在每次请求时将JWT放入HTTP的Header中的Authorization位。(解决XSS和XSRF问题）HEADER
    后端检查是否存在，如存在验证JWT的有效性。例如，检查签名是否正确﹔检查Token是否过期;检查Token的接收方是否是自己(可选）
    
  * 验证通过后后端使用JWT中包含的用户信息进行其他逻辑操作，返回相应结果。
  
    ```java
    @Component
    @Slf4j
    public class JWTProvider {
        private Key key;	// 私钥
        private long tokenValidityInMilliseconds; // 有效时间
        private long tokenValidityInMillisecondsForRememberMe; // 记住我有效时间
        @Autowired
        private JJWTProperties jjwtProperties; // jwt配置参数
        @Autowired
        private UserRepository userRepository; 
        @PostConstruct
        public void init() {
            byte[] keyBytes;
            String secret = jjwtProperties.getSecret();
            if (StringUtils.hasText(secret)) {
                log.warn("Warning: the JWT key used is not Base64-encoded. " +
                        "We recommend using the `jhipster.security.authentication.jwt.base64-secret` key for optimum security.");
                keyBytes = secret.getBytes(StandardCharsets.UTF_8);
            } else {
                log.debug("Using a Base64-encoded JWT secret key");
                keyBytes = Decoders.BASE64.decode(jjwtProperties.getBase64Secret());
            }
            this.key = Keys.hmacShaKeyFor(keyBytes); // 使用mac-sha算法的密钥
            this.tokenValidityInMilliseconds =
                    1000 * jjwtProperties.getTokenValidityInSeconds();
            this.tokenValidityInMillisecondsForRememberMe =
                    1000 * jjwtProperties.getTokenValidityInSecondsForRememberMe();
        }
        public String createToken(Authentication authentication, boolean rememberMe) {
            long now = (new Date()).getTime();
            Date validity;
            if (rememberMe) {
                validity = new Date(now + this.tokenValidityInMillisecondsForRememberMe);
            } else {
                validity = new Date(now + this.tokenValidityInMilliseconds);
            }
            User user = userRepository.findOneByLogin(authentication.getName());
            Map<String ,Object> map = new HashMap<>();
            map.put("sub",authentication.getName());
            map.put("user",user);
            return Jwts.builder()
                    .setClaims(map) // 添加body
                    .signWith(key, SignatureAlgorithm.HS512) // 指定摘要算法
                    .setExpiration(validity) // 设置有效时间
                    .compact();
        }
        public Authentication getAuthentication(String token) {
            Claims claims = Jwts.parserBuilder()
                    .setSigningKey(key)
                    .build()
                    .parseClaimsJws(token).getBody(); // 根据token获取body
            User principal;
            Collection<? extends GrantedAuthority> authorities;
            principal = userRepository.findOneByLogin(claims.getSubject());
            authorities = principal.getAuthorities();
            return new UsernamePasswordAuthenticationToken(principal, token, authorities);
        }
    }
    
    ```
  
    > 注意这里我们创建的User需要实现UserDetails对象，这样我们可以根据`principal.getAuthorities()`获取到权限，如果不实现UserDetails，那么需要自定义authorities并添加到UsernamePasswordAuthenticationToken中。
  
    ```typescript
    @Data
    @Entity
    @Table(name="user")
    public class User implements UserDetails {
        @Id
        @Column
        private Long id;
        @Column
        private String login;
        @Column
        private String password;
        @Column
        private String role;
        @Override
        // 获取权限，这里就用简单的方法
        // 在spring security中，Authorities既可以是ROLE也可以是Authorities
        public Collection<? extends GrantedAuthority> getAuthorities() {
            return Collections.singleton(new SimpleGrantedAuthority(role));
        }
        @Override
        public String getUsername() {
            return login;
        }
        @Override
        public boolean isAccountNonExpired() {
            return true;
        }
        @Override
        public boolean isAccountNonLocked() {
            return false;
        }
        @Override
        public boolean isCredentialsNonExpired() {
            return true;
        }
        @Override
        public boolean isEnabled() {
            return true;
        }
    }
    ```
  
    #### 创建登录成功，登出成功处理器
  
    > 登录成功后向前台发送jwt。
  
    认证成功，返回jwt：
  
    ```java
    public class MyAuthenticationSuccessHandler implements AuthenticationSuccessHandler{
        void onAuthenticationSuccess(HttpServletRequest request, HttpServletResponse response, Authentication authentication) throws IOException, ServletException{
            PrintWriter writer = response.getWriter();
            writer.println(jwtProvider.createToken(authentication, true));
        }
    }
    ```
  
    登出成功：
  
    ```java
    public class MyLogoutSuccessHandler implements LogoutSuccessHandler {
        void onLogoutSuccess(HttpServletRequest var1, HttpServletResponse var2, Authentication var3) throws IOException, ServletException{
            PrintWriter writer = response.getWriter();
            writer.println("logout success");
            writer.flush();
        }
    }
    ```
  
    #### 设置登录、登出、取消csrf防护
  
    > 登出无法对token进行失效操作，可以使用数据库保存token，然后在登出时删除该token。
  
    ```scala
    @Configuration
    public class MySecurityConfiguration extends WebSecurityConfigurerAdapter {
        // code...
        @Override
        protected void configure(HttpSecurity http) throws Exception {
           http
               // code...
               // 添加登录处理器
               .formLogin().loginProcessingUrl("/login").successHandler((request, response, authentication) -> {
               PrintWriter writer = response.getWriter();
               writer.println(jwtProvider.createToken(authentication, true));
           })
               // 取消csrf防护
               .and().csrf().disable() 
               // code...
               // 添加登出处理器
               .and().logout().logoutUrl("/logout").logoutSuccessHandler((HttpServletRequest request, HttpServletResponse response, Authentication authentication) -> {
               PrintWriter writer = response.getWriter();
               writer.println("logout success");
               writer.flush();
           })
            	// code...
        }
        // code...
    }
    ```
  
    #### 使用JWT集成spring-security
  
    > 添加Filter供spring-security解析token，并向securityContext中添加我们的用户信息。
    >
    > 在UsernamePasswordAuthenticationFilter.class之前我们需要执行根据token添加authentication。关键方法是从jwt中获取authentication，然后添加到securityContext中。
    >
    > 在SecurityConfiguration中需要设置Filter添加的位置。
  
    创建自定义Filter，用于jwt获取authentication：
  
    ```java
    @Slf4j
    public class JWTFilter extends GenericFilterBean {
    
        private final static String HEADER_AUTH_NAME = "auth";
    
        private JWTProvider jwtProvider;
    
        public JWTFilter(JWTProvider jwtProvider) {
            this.jwtProvider = jwtProvider;
        }
    
        @Override
        public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
            try {
                HttpServletRequest httpServletRequest = (HttpServletRequest) servletRequest;
                String authToken = httpServletRequest.getHeader(HEADER_AUTH_NAME);
                if (StringUtils.hasText(authToken)) {
                    // 从自定义tokenProvider中解析用户
                    Authentication authentication = this.jwtProvider.getAuthentication(authToken);
                    SecurityContextHolder.getContext().setAuthentication(authentication);
                }
                // 调用后续的Filter,如果上面的代码逻辑未能复原“session”，SecurityContext中没有想过信息，后面的流程会检测出"需要登录"
                filterChain.doFilter(servletRequest, servletResponse);
            } catch (Exception ex) {
                throw new RuntimeException(ex);
            }
        }
    }
    ```
  
    向HttpSecurity添加Filter和设置Filter位置：
  
    ```scala
    public class MySecurityConfiguration extends WebSecurityConfigurerAdapter {
        // code...
        @Override
        protected void configure(HttpSecurity http) throws Exception {
            http
                    .sessionManagement()
                	//设置添加Filter和位置
                    .and().addFilterBefore(new JWTFilter(jwtProvider), UsernamePasswordAuthenticationFilter.class);
                    // code...
        }
        // code...
    }
    ```
  
    #### MySecurityConfiguration代码
  
    ```java
    @Configuration
    @EnableGlobalMethodSecurity(prePostEnabled = true)
    public class MySecurityConfiguration extends WebSecurityConfigurerAdapter {
        @Autowired
        private UserDetailsService userDetailsService;
        @Autowired
        private JWTProvider jwtProvider;
        @Override
        protected void configure(AuthenticationManagerBuilder auth) throws Exception {
            auth.userDetailsService(userDetailsService)// 设置自定义的userDetailsService
                    .passwordEncoder(passwordEncoder());
        }
        @Override
        protected void configure(HttpSecurity http) throws Exception {
            http
                    .sessionManagement()
                    .sessionCreationPolicy(SessionCreationPolicy.STATELESS)//设置无状态
                    .and()
                    .authorizeRequests() // 配置请求权限
                    .antMatchers("/product/**").hasRole("USER") // 需要角色
                    .antMatchers("/admin/**").hasRole("ADMIN")
                    .anyRequest().authenticated() // 所有的请求都需要登录
                    .and()
                	// 配置登录url，和登录成功处理器
                    .formLogin().loginProcessingUrl("/login").successHandler((request, response, authentication) -> {
                        PrintWriter writer = response.getWriter();
                        writer.println(jwtProvider.createToken(authentication, true));
                    })
                	// 取消csrf防护
                    .and().csrf().disable() 
                    .httpBasic()
                	// 配置登出url，和登出成功处理器
    				.and().logout().logoutUrl("/logout")
                	.logoutSuccessHandler((HttpServletRequest request, HttpServletResponse response, Authentication authentication) -> {
                        PrintWriter writer = response.getWriter();
                        writer.println("logout success");
                        writer.flush();
                    })
                	// 在UsernamePasswordAuthenticationFilter之前执行我们添加的JWTFilter
                    .and().addFilterBefore(new JWTFilter(jwtProvider), UsernamePasswordAuthenticationFilter.class);
        }
        @Bean
        public PasswordEncoder passwordEncoder() {
            return NoOpPasswordEncoder.getInstance();
        }
        @Override
        public void configure(WebSecurity web) {
            // 添加不做权限的URL
            web.ignoring()
                    .antMatchers("/swagger-resources/**")
                    .antMatchers("/swagger-ui.html")
                    .antMatchers("/webjars/**")
                    .antMatchers("/v2/**")
                    .antMatchers("/h2-console/**");
        }
    }
    ```
  
    #### 使用注解对方法进行权限管理
  
    > 需要在`MySecurityConfiguration`上添加`@EnableGlobalMethodSecurity(prePostEnabled = true)`注解，prePostEnabled默认为false，需要设置为true后才能全局的注解权限控制。
  
    prePostEnabled设置为true后，可以使用四个注解：
  
    添加实体类School：
  
    ```typescript
    @Data
    public class School implements Serializable {
        private Long id;
        private String name;
        private String address;
    }
    ```
  
    - @PreAuthorize
  
      在访问之前就进行权限判断
  
      ```kotlin
      @RestController
      public class AnnoController {
          @Autowired
          private JWTProvider jwtProvider;
          @RequestMapping("/annotation")
      //    @PreAuthorize("hasRole('ADMIN')")
          @PreAuthorize("hasAuthority('ROLE_ADMIN')")
          public String info(){
              return "拥有admin权限";
          }
      }
      ```
  
      hasRole和hasAuthority都会对UserDetails中的getAuthorities进行判断区别是hasRole会对字段加上`ROLE_`后再进行判断，上例中使用了`hasRole('ADMIN')`，那么就会使用`ROLE_ADMIN`进行判断，如果是`hasAuthority('ADMIN')`，那么就使用`ADMIN`进行判断。
  
    - @PostAuthorize
  
      在请求之后进行判断，如果返回值不满足条件，会抛出异常，但是方法本身是已经执行过了的。
  
      ```kotlin
      @RequestMapping("/postAuthorize")
      @PreAuthorize("hasRole('ADMIN')")
      @PostAuthorize("returnObject.id%2==0")
      public School postAuthorize(Long id) {
          School school = new School();
          school.setId(id);
          return school;
      }
      ```
  
      returnObject是内置对象，引用的是方法的返回值。
  
      如果`returnObject.id%2==0`为 true，那么返回方法值。如果为false，会返回403 Forbidden。
  
    - @PreFilter
  
      在方法执行之前，用于过滤集合中的值。
  
      ```less
      @RequestMapping("/preFilter")
      @PreAuthorize("hasRole('ADMIN')")
      @PreFilter("filterObject%2==0")
      public List<Long> preFilter(@RequestParam("ids") List<Long> ids) {
          return ids;
      }
      ```
  
      `filterObject`是内置对象，引用的是集合中的泛型类，如果有多个集合，需要指定`filterTarget`。
  
      ```less
      @PreFilter(filterTarget="ids", value="filterObject%2==0")
      public List<Long> preFilter(@RequestParam("ids") List<Long> ids,@RequestParam("ids") List<User> users,) {
          return ids;
      }
      ```
  
      `filterObject%2==0`会对集合中的值会进行过滤，为true的值会保留。
  
      第一个例子返回的值在执行前过滤返回2，4。
  
      [![image-20201202115120854](jwt.assets/t_201208012605image-20201202115120854.png)](https://images.cnblogs.com/cnblogs_com/dl610455894/1895651/t_201208012605image-20201202115120854.png)
  
    - @PostFilter
  
      会对返回的集合进行过滤。
  
      ```mipsasm
      @RequestMapping("/postFilter")
      @PreAuthorize("hasRole('ADMIN')")
      @PostFilter("filterObject.id%2==0")
      public List<School> postFilter() {
          List<School> schools = new ArrayList<School>();
          School school;
          for (int i = 0; i < 10; i++) {
              school = new School();
              school.setId((long)i);
              schools.add(school);
          }
          return schools;
      }
      ```
  
      上面的方法返回结果为：id为0，2，4，6，8的School对象。