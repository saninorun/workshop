from sqlalchemy import select, union_all
from ..dbtable.dbmodel import   ProductBD, DiscountCardsBD, DiscountCardsHistoryBD, \
                                ProductPriceBD


class Query:
    query_unused_card = select(  
                            DiscountCardsBD,                                            
                            ).join(
                                DiscountCardsHistoryBD, isouter=True,
                                ).where(                    
                                    DiscountCardsHistoryBD.cardnumber_id == None          
                                    )    

    query_free_used_card = select(  
                            DiscountCardsBD,                                            
                            ).join(
                                DiscountCardsHistoryBD
                                ).where(                    
                                    DiscountCardsHistoryBD.date_stop_use != None          
                                    ) 

    query_card_for_newcustomer = select(
                            DiscountCardsBD,
                            ).from_statement(
                                    union_all(
                                        query_unused_card,
                                        query_free_used_card,
                                        ).order_by(
                                            DiscountCardsBD.cardnumber.asc()
                                            )
                                )
    
    query_www = select(
                    ProductPriceBD
                    ).join(
                        ProductBD
                        )