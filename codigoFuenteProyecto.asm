

.DATA
                       
    VAR_DEC    DB 25             
    VAR_HEX    DW 0FFH           
    VAR_BIN    DB 10101010B      
    MENSAJE    DB "HOLA", '$'    
    CTE_EQU    EQU 100           
    ARRAY      DB 5 DUP(0)       
    
    
    VAR1       DB 10             
    VAR_MAL    DB 255            
    HEX_ERROR  DW 0AFH           
    BIN_ERROR  DB 1010B          
    EQU_MAL    EQU 100           

.CODE
START:
    
    MOV AX, @DATA
    MOV DS, AX

    CBW                          
                         
    CLC                          
    LODSB                        
    AAA                          
    
    
    PUSH CX                      
    POP AX                       
    POP [SI]                     
                      
    
    
    MOV AX, 10                   
    MOV BL, 2                    
    IDIV BL                      
                         
    
    
    AND AX, BX                   
    AND AX, 5                    
                     
    
    ADC AL, 10                   
    LEA BX, VAR_DEC              
                    
    
    LES DI, [SI]                 
    

    JZ ETIQUETA_OK               
                     
    JB SALTO_VALIDO              
    
    
    LOOPNZ SIGUIENTE             
    INT 21H                      
                         

    
    JGE ETIQUETA_1               
    JNA ETIQUETA_2               
    JNL ETIQUETA_3               

ETIQUETA_OK:
SIGUIENTE:
SALTO_VALIDO:
ETIQUETA_1:
ETIQUETA_2:
ETIQUETA_3:

    
    MOV AH, 4CH
    INT 21H

END START