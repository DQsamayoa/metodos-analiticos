library(feather)
library(tidyverse)
library(aws.s3)

datos_path <- "datos/"

cubeta <- "metodos-analiticos/proyecto_final/datos"

categorias_path <- list.files(datos_path) %>% 
                   grep(pattern = ".csv", value = TRUE, invert = TRUE) %>% 
                   str_replace_all(pattern = "_", replacement = "-")

categorias_path %>% 
  map(function(categoria) {
    path <- paste0(datos_path, categoria)
    
    datos <- list.files(path, pattern = "*.feather") %>% 
      paste0(path, "/", .) %>% 
      map_dfr(read_feather)
    
    datos_file <- paste0(path, ".csv")
    
    datos %>% 
      write_csv(datos_file)
    
    put_object(datos_file, object = paste0(categoria, ".csv"), bucket = cubeta,
               multipart = TRUE, verbose = TRUE, show_progress = TRUE)
  })