# syntax=docker/dockerfile:1

##########################
# Backend build stage
##########################
FROM eclipse-temurin:17-jdk AS backend-builder                                                                           
WORKDIR /aitrace/backend/aitrace-java-backend                                                                                      
                                                                                                                         
COPY backend/aitrace-java-backend/gradle ./gradle                                                                          
COPY backend/aitrace-java-backend/gradlew backend/aitrace-java-backend/build.gradle backend/aitrace-java-backend/settings.gradle ./                                                                                              
RUN chmod +x gradlew                                                                                               
RUN ./gradlew --no-daemon dependencies                                                                                   
                                                                                                                         
COPY backend/aitrace-java-backend/src ./src                                                                                
RUN ./gradlew --no-daemon bootJar -x test                                                                                
                                                                                                                         
##########################                                                                                               
# Backend runtime stage                                                                                                  
##########################                                                                                               
FROM eclipse-temurin:17-jre AS backend-runtime                                                                           
WORKDIR /aitrace                                                                                                 
ENV SPRING_PROFILES_ACTIVE=prod \                                                                                        
    JAVA_OPTS="-Xms512m -Xmx1024m"                                                                                       
COPY --from=backend-builder /aitrace/backend/aitrace-java-backend/build/libs/*.jar /aitrace/backend/aitrace-java-backend/app.jar                                                   
EXPOSE 8080                                                                                                              
ENTRYPOINT ["sh","-c","java $JAVA_OPTS -jar /aitrace/backend/aitrace-java-backend/app.jar"]                                                               
                                                                                                                         
##########################                                                                                               
# Web build stage                                                                                                        
##########################                                                                                               
FROM node:20-bullseye AS web-builder                                                                                     
WORKDIR /aitrace/web                                                                                                         
ENV NODE_ENV=production                                                                                                  
                                                                                                                         
COPY web/package*.json ./                                                                                             
RUN npm ci                                                                                                               
                                                                                                                         
COPY web ./                                                                                                           
RUN npm run build                                                                                                        
                                                                                                                         
##########################
# Web runtime stage                                                                                                      
##########################                                                                                               
FROM nginx:1.27-alpine AS web-runtime                                                                                    
ENV BACKEND_HOST=backend BACKEND_PORT=8080                                                                              
RUN rm /etc/nginx/conf.d/default.conf && mkdir -p /etc/nginx/templates                                                  
COPY docker/nginx/nginx.conf /etc/nginx/templates/default.conf.template                                                
COPY --from=web-builder /aitrace/web/dist /usr/share/nginx/html                                                        
EXPOSE 80                                                                                                               
CMD ["nginx","-g","daemon off;"]                                                                                         
                                                                                                                         
# Default target is the backend image; build the web image with --target web-runtime                                     
FROM backend-runtime      
