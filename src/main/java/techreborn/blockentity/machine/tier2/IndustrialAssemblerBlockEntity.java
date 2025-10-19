/*
 * This file is part of TechReborn, licensed under the MIT License (MIT).
 *
 * Copyright (c) 2025 TechReborn
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package techreborn.blockentity.machine.tier2;

import net.minecraft.block.BlockState;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.util.math.BlockPos;
import reborncore.common.recipes.RecipeCrafter;
import reborncore.common.screen.BuiltScreenHandler;
import reborncore.common.screen.BuiltScreenHandlerProvider;
import reborncore.common.screen.builder.ScreenHandlerBuilder;
import reborncore.common.util.RebornInventory;
import techreborn.blockentity.machine.GenericMachineBlockEntity;
import techreborn.config.TechRebornConfig;
import techreborn.init.ModRecipes;
import techreborn.init.TRBlockEntities;
import techreborn.init.TRContent;

public class IndustrialAssemblerBlockEntity extends GenericMachineBlockEntity implements BuiltScreenHandlerProvider {

	public IndustrialAssemblerBlockEntity(BlockPos pos, BlockState state) {
		super(TRBlockEntities.INDUSTRIAL_ASSEMBLER, pos, state, "IndustrialAssembler", TechRebornConfig.industrialAssemblerMaxInput, TechRebornConfig.industrialAssemblerMaxEnergy, TRContent.Machine.INDUSTRIAL_ASSEMBLER.block, 5);
		final int[] inputs = new int[]{0, 1, 2, 3};
		final int[] outputs = new int[]{4};
		this.inventory = new RebornInventory<>(6, "IndustrialAssemblerBlockEntity", 64, this);
		this.crafter = new RecipeCrafter(ModRecipes.INDUSTRIAL_ASSEMBLER, this, 4, 1, this.inventory, inputs, outputs);
	}

	@Override
	public BuiltScreenHandler createScreenHandler(int syncID, PlayerEntity player) {
		return new ScreenHandlerBuilder("industrialassembler").player(player.getInventory()).inventory().hotbar()
			.addInventory().blockEntity(this)
			.slot(0, 45, 35).slot(1, 45, 55)
			.slot(2, 65, 35).slot(3, 65, 55)
			.outputSlot(4, 111, 45).energySlot(5, 8, 72)
			.syncEnergyValue().syncCrafterValue().addInventory().create(this, syncID);
	}
}
