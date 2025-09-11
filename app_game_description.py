import streamlit as st
def game_info():
    highlight_color = "#F15922"

    st.subheader("**Introduction** 🏭")
    st.markdown(f"<hr style='border:1px solid {highlight_color}; margin:0px 0'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align: justify;'>
    Step into the role of a factory manager in this interactive mini-factory simulation. Your objective is to optimize production, quality, cost, and sustainability while delivering products on time. This hands-on game demonstrates the challenges of modern manufacturing management, where every decision has a direct impact on profitability, efficiency, and environmental performance.
    <div style='text-align: justify; margin-top:10px;'>
    </div>
    """, unsafe_allow_html=True)

    st.image("picture_Factory.jpg", use_container_width=True)

    st.subheader("**Game Description** 📋")
    st.markdown(f"<hr style='border:1px solid {highlight_color}; margin:0px 0'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align: justify;'>
    In this game, you run a mini-factory <b><span style='color:{highlight_color}'>producing gears (T100), assembling pins to base plates (T200), assembling gears onto base pallets (T800),</span></b> packaging, palletizing using two robots (Robot #01 and Robot #02), and shipping the finished products to your customer. The target is to deliver <b><span style='color:{highlight_color}'>1000 good quality products</span></b> at a fixed price of <b><span style='color:{highlight_color}'>€ 4.78 per product</span></b> within a <b><span style='color:{highlight_color}'>14 hours production window.</span></b> Your performance will be measured by <b><span style='color:{highlight_color}'>profit.</span></b>
    <div style='text-align: justify; margin-top:20px;'>
    </div>
    """, unsafe_allow_html=True)

         

    st.markdown(f"""
    <div style='text-align: justify;'>
    <div style='text-align: justify; margin-top:0px;'>
    <b><span style='color:{highlight_color}'>Revenue comes from the products sold, while expenses are calculated based on:</span></b>
    <ul>
    <li>Operator hourly wages</li>
    <li>Energy consumption</li>
    <li>Raw material costs (pins, base plates, and rods)</li>
    <li>Packaging costs (retailer boxes, shipping boxes, pallets)</li>
    <li>Shipping costs</li>
    </ul>

    <div style='text-align: justify; margin-top:20px;'>
        <b><b><span style='color:{highlight_color}'>Penalties apply for the following production failures:</span></b>
    <ul>
    <li>Late delivery: Orders delayed up to 15% incur minor penalties; beyond 15%, severe financial penalties apply.</li>
    <li>Insufficient delivered product: The shortfall compared to the ordered quantity incurs a significant monetary penalty per unit.</li>
    <li>Excess production: Extra products are charged per unit, with reject quality products costing more than good quality products.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    
    st.image("picture_Layout_with_Texts.jpg", use_container_width=True)

    st.subheader("**Adjustable Parameters** ⚙️")
    st.markdown(f"<hr style='border:1px solid {highlight_color}; margin:0px 0'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align: justify;'>
    You can adjust 7 key parameters to optimize your production strategy:

    <div style='text-align: justify; margin-top:10px;'>
    <div style='text-align: justify;'>
    <b><span style='color:{highlight_color}'>1.</span> <span style='color:{highlight_color}'>Size of the batches (8 / 24 / 40 pcs)</span></b><br>
    <i>Small ⟶ faster start but more changeovers<br></i>
    <i>Large ⟶ fewer changeovers but slower start</i>
    </div>

    <div style='text-align: justify; margin-top:10px;'>            
    <div style='text-align: justify;'>
    <b><span style='color:{highlight_color}'>2.</span> <span style='color:{highlight_color}'>Size of the shipping box (18 / 30 / 50 pcs)</span></b><br>
    <i>Small ⟶ lower price, more boxes, more pallets<br></i>
    <i>Large ⟶ higher price, fewer boxes, fewer pallets</i>
    </div>

    <div style='text-align: justify; margin-top:10px;'>
    <div style='text-align: justify;'>
    <b><span style='color:{highlight_color}'>3.</span> <span style='color:{highlight_color}'>Machine - cycle time factor (−20% … +20%)</span></b><br>
    <i>Faster ⟶ higher output, but lower availability, more rejects, higher energy, and more operator demands<br></i>
    <i>Slower ⟶ lower output, but higher availability, fewer rejects, lower energy, and fewer operator demands</i>
    </div>

    <div style='text-align: justify; margin-top:10px;'>
    <div style='text-align: justify;'>
    <b><span style='color:{highlight_color}'>4.</span> <span style='color:{highlight_color}'>Number of the operators (1 / 2 / 3 operators)</span></b><br>
    <i>Fewer operators ⟶ lower cost but higher downtime risk<br></i>
    <i>More operators ⟶ higher cost but smoother production flow</i>
    </div>

    <div style='text-align: justify; margin-top:10px;'>
    <div style='text-align: justify;'>
    <b><span style='color:{highlight_color}'>5.</span> <span style='color:{highlight_color}'>Type of quality check</span></b><br>
    <i>At each station ⟶ higher operator demand but fewer rejects<br></i>
    <i>End-of-line ⟶ lower operator demand but denser rejects</i>
    </div>

                
    <div style='text-align: justify; margin-top:10px;'>
    <div style='text-align: justify;'>
    <b><span style='color:{highlight_color}'>6.</span> <span style='color:{highlight_color}'>Percentage of the quality check (0–100%)</span></b><br>
    <i>Low percentage ⟶ less operator demand, outgoing more rejects<br></i>
    <i>High percentage ⟶ higher operator demand, outgoing fewer rejects</i>
    </div>

    <div style='text-align: justify; margin-top:10px;'>
    <div style='text-align: justify;'>
    <b><span style='color:{highlight_color}'>7.</span> <span style='color:{highlight_color}'>Overshooting (0 / 10 / 20%)</span></b><br>
    <i>Extra production to ensure 1000 good products even if rejects occur.</i>
    <div style='text-align: justify; margin-top:20px;'>
    </div>

    """, unsafe_allow_html=True)

    st.image("picture_Detailed_01.jpg", use_container_width=True)

    st.subheader("**Additional Information** ℹ️")
    st.markdown(f"<hr style='border:1px solid {highlight_color}; margin:0px 0'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align: justify;'>
    <ul>
    <li>Infinite storage for raw materials, boxes, and pallets – no deadlocks.</li>
    <li>Strategic trade-offs between speed, cost, quality, and sustainability will determine your overall success.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("**Game Goal** 🎯")
    st.markdown(f"<hr style='border:1px solid {highlight_color}; margin:0px 0'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align: justify;'>
    Your goal is to find the sweet spot between <b><span style='color:{highlight_color}'>speed, quality, cost, and sustainability to maximize your profit</span></b> while maintaining the production schedule.
    <div style='text-align: justify; margin-top:20px;'>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("**Ready to Play?** 🕹️")
    st.markdown(f"<hr style='border:1px solid {highlight_color}; margin:0px 0'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align: justify;'>
    Adjust the parameters and monitor production to maximize your profit. You have <b><span style='color:{highlight_color}'>5 attempts</span></b> to earn the highest profit. Don’t forget to click the <b><span style='color:{highlight_color}'>“Finish the Game” </span></b> button when you’re done to see your <b><span style='color:{highlight_color}'>rank on the current leaderboard!</span></b>
    <div style='text-align: justify; margin-top:20px;'>
    </div>
    """, unsafe_allow_html=True)
