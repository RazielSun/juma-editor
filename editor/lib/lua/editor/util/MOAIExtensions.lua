--------------------------------------------------------------------------------
-- Extensions for default MOAI objects
-- 
-- 
-- 
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
-- Common overrides for all prop subclasses
--------------------------------------------------------------------------------

local function initPropInterface ( interface, superInterface )

    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    function interface.setParent ( self, parent, onlyLoc )

        self.parent = parent

        superInterface.clearAttrLink ( self, MOAIColor.INHERIT_COLOR )
        superInterface.clearAttrLink ( self, MOAITransform.INHERIT_TRANSFORM )
        superInterface.clearAttrLink ( self, MOAIProp.INHERIT_VISIBLE )
        superInterface.clearAttrLink ( self, MOAITransform.INHERIT_LOC )

        if parent then
            superInterface.setAttrLink ( self, MOAIColor.INHERIT_COLOR, parent, MOAIColor.COLOR_TRAIT )
            superInterface.setAttrLink ( self, MOAIProp.INHERIT_VISIBLE, parent, MOAIProp.ATTR_VISIBLE )
            if onlyLoc then
                superInterface.setAttrLink ( self, MOAITransform.INHERIT_LOC, parent, MOAITransform.TRANSFORM_TRAIT )
            else
                superInterface.setAttrLink ( self, MOAITransform.INHERIT_TRANSFORM, parent, MOAITransform.TRANSFORM_TRAIT )
            end
        end
    end

    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    function interface.getVisible ( self )
        return superInterface.getAttr ( self, MOAIProp.ATTR_VISIBLE ) > 0
    end

    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    function interface.setScissorRect ( self, scissorRect )
        self.scissorRect = scissorRect
        superInterface.setScissorRect ( self, scissorRect )
    end
    
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    function interface.getWorldDims ( self )
        local xMin, yMin, zMin, xMax, yMax, zMax = superInterface.getWorldBounds ( self )
        if not xMin then return end
        return xMax - xMin, yMax - yMin, zMax - zMin
    end

    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    function interface.setRelPiv ( self, x, y, z )
        x = x or 0
        y = y or 0
        z = z or 0
        local w, h, d = superInterface.getDims ( self )
        superInterface.setPiv ( self, x * w, y * h, z * d )
    end
end


--------------------------------------------------------------------------------
-- MOAIProp
--------------------------------------------------------------------------------

MOAIProp.extend (

    'MOAIProp',
    
    --------------------------------------------------------------------------------
    function ( interface, class, superInterface, superClass )
        initPropInterface ( interface, superInterface )
        
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        function interface.setLayer ( self, layer )

            if self.layer == layer then
                return
            end

            if self.layer then
                self.layer:removeProp ( self )
                if self.layer._propShader then
                    superInterface.clearAttrLink ( self, MOAIProp.ATTR_SHADER )
                end
            end

            self.layer = layer

            if self.layer then
                layer:insertProp ( self )
                if layer._propShader then
                    superInterface.setAttrLink ( self, MOAIProp.ATTR_SHADER, layer._propShader, MOAIProp.ATTR_SHADER )
                end
            end
        end

        -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        -- function interface.setTexture ( self, texture )

        -- end

        -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        function interface.setIndexByName ( self, name )

            if type(name) == "string" then
                local deck = self.deck or self:getDeck()
                local index = deck and deck.names and deck.names[name]
                if index then
                    self:setIndex(index)
                end
            end
        end

        -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        function interface.fitToSize ( self, width, height, smin, smax )
            local w, h = superInterface.getDims ( self )
            local s
            
            if width and height then
                local s1 = width / w
                local s2 = height / h
                s = s1 < s2 and s1 or s2
            elseif width then
                s = width / w
            elseif height then
                s = height / h
            end

            s = math.clamp(s, smin or s, smax or s)
            if s then
                superInterface.setScl ( self, s, s, 1 )
            end
        end

        -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        function interface.scaleToSize ( self, width, height )
            local w, h = superInterface.getDims ( self )
            superInterface.setScl ( self, width / w, height / h, 1 )
        end

        -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        function interface.setFlip ( self, x, y )
            
        end
    end
)

--------------------------------------------------------------------------------
-- MOAILayer
--------------------------------------------------------------------------------

MOAILayer.extend (

    'MOAILayer',
    
    --------------------------------------------------------------------------------
    function ( interface, class, superInterface, superClass )
        initPropInterface ( interface, superInterface )
        
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        function interface.setLayer ( self, layer )
            -- nested layers not supported
        end
    end
)

-- MOAITimer.extend (

--     'MOAITimer',
        
--     ----------------------------------------------------------------
--     function ( interface, class, superInterface, superClass )
        
--         -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -
--         -- extend the class
--         local new = class.new
        
--         function class.new ()
--             local self = new ()
--             local str = "MOAITimer: \n" .. debug.traceback()
--             superInterface.setDebugInfo ( self, str )
--             return self
--         end
--     end
-- )


--------------------------------------------------------------------------------
-- MOAITextBox
--------------------------------------------------------------------------------

MOAITextBox.extend (

    'MOAITextBox', 

    --------------------------------------------------------------------------------
    function ( interface, class, superInterface, superClass )
        initPropInterface ( interface, superInterface )
        
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        function interface.setLayer ( self, layer )

            if self.layer == layer then
                return
            end

            if self.layer then
                self.layer:removeProp ( self )
                if self.layer._textShader then
                    superInterface.clearAttrLink ( self, MOAIProp.ATTR_SHADER )
                end
            end

            self.layer = layer

            if self.layer then
                layer:insertProp ( self )
                if layer._textShader then
                    superInterface.setAttrLink ( self, MOAIProp.ATTR_SHADER, layer._textShader, MOAIProp.ATTR_SHADER )
                end
            end
        end
    end

)

--------------------------------------------------------------------------------
-- MOAISpineSkeleton
--------------------------------------------------------------------------------
if MOAISpineSkeleton then
    
    MOAISpineSkeleton.extend (

        'MOAISpineSkeleton', 

        --------------------------------------------------------------------------------
        function ( interface, class, superInterface, superClass )
            initPropInterface ( interface, superInterface )
            
            local new = class.new
            -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            function class.new ()
                -- set shader explicitly to workaround gfx state flushing bug
                local self = new ()
                self:setShader ( MOAIShaderMgr.getShader ( MOAIShaderMgr.DECK2D_SHADER ))
                return self
            end

            -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            function interface.setLayer ( self, layer )

                if self.layer == layer then
                    return
                end

                if self.layer then
                    self.layer:removeProp ( self )
                end

                self.layer = layer

                if self.layer then
                    layer:insertProp ( self )
                end
            end
        end

    )
end

--------------------------------------------------------------------------------
-- MOAIParticleSystem
--------------------------------------------------------------------------------
MOAIParticleSystem.extend (
    'MOAIParticleSystem', 

    --------------------------------------------------------------------------------
    function ( interface, class, superInterface, superClass )
        initPropInterface ( interface, superInterface )
        
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        function interface.setLayer ( self, layer )

            if self.layer == layer then
                return
            end

            if self.layer then
                self.layer:removeProp ( self )
            end

            self.layer = layer

            if self.layer then
                layer:insertProp ( self )
            end
        end
    end
)
